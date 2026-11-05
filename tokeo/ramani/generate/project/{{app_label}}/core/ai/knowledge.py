"""
The knowledge index of the {{ app_name }} ai examples: a small, local RAG.

It reads the text files (```.md```, ```.txt```) below a directory, splits them
into sections at blank lines (a heading stays with the text below it), and
ranks the sections for a query by BM25: rare words count more, long sections
are not preferred. No server and no extra dependency; the index lives in
memory and is built again when a file changes.

Two examples share it: the retrieve transformer puts the best sections in
front of the prompt at ```on_prompt```, the tool ```search_docs``` lets the
model ask for them itself.
"""

import os
import re
import math
import threading
from dataclasses import dataclass

#: The file suffixes the index reads.
KNOWLEDGE_FILE_SUFFIXES = ('.md', '.txt')

#: The BM25 parameters: term saturation and length normalization.
BM25_K1 = 1.5
BM25_B = 0.75


@dataclass
class KnowledgeHit:
    """
    A section found for a query.

    ### Args

    - **source** (str): The file, relative to the index directory
    - **section** (int): The number of the section in the file, from 1
    - **score** (float): The BM25 score, higher is better
    - **text** (str): The text of the section

    """

    source: str
    section: int
    score: float
    text: str


class KnowledgeIndex:
    """
    A BM25 index over the sections of the text files below a directory.

    ### Args

    - **base_dir** (str): The directory to read, relative to the working
        directory or absolute

    """

    # one index per directory and process, built again when a file changes
    _indexes = {}
    _lock = threading.Lock()

    def __init__(self, base_dir):
        self.base_dir = os.path.abspath(base_dir)
        self.signature = None
        self.sections = []
        self.lengths = []
        self.counts = []
        self.idf = {}

    @classmethod
    def of(cls, base_dir):
        """
        Return the up-to-date index of a directory.

        ### Args

        - **base_dir** (str): The directory to read

        ### Returns

        - **KnowledgeIndex**: The index, built again if a file was added,
            removed or changed since the last call

        """
        with cls._lock:
            index = cls._indexes.setdefault(os.path.abspath(base_dir), cls(base_dir))
            files = index.files()
            signature = [(path, os.stat(path).st_mtime_ns, os.stat(path).st_size) for path in files]
            if signature != index.signature:
                index.build(files)
                index.signature = signature
            return index

    def files(self):
        """
        List the text files below the directory, sorted.

        ### Returns

        - **list[str]**: The absolute paths; empty when the directory is missing

        """
        found = []
        for root, _, names in os.walk(self.base_dir):
            found += [os.path.join(root, name) for name in names if name.endswith(KNOWLEDGE_FILE_SUFFIXES)]
        return sorted(found)

    def build(self, files):
        """
        Split the files into sections and count their words.

        ### Args

        - **files** (list[str]): The absolute paths to read

        """
        self.sections, self.lengths, self.counts = [], [], []
        for path in files:
            with open(path, encoding='utf-8') as f:
                blocks = [block.strip() for block in re.split(r'\n\s*\n', f.read()) if block.strip()]
            source = os.path.relpath(path, self.base_dir)
            number, heading = 0, ''
            for block in blocks:
                # a heading alone belongs to the text below it
                if block.startswith('#') and '\n' not in block:
                    heading = f'{heading}\n{block}'.strip()
                    continue
                number += 1
                text = f'{heading}\n{block}'.strip()
                heading = ''
                words = re.findall(r'\w+', text.lower())
                counts = {}
                for word in words:
                    counts[word] = counts.get(word, 0) + 1
                self.sections.append((source, number, text))
                self.lengths.append(len(words))
                self.counts.append(counts)
        total = len(self.sections)
        df = {}
        for counts in self.counts:
            for word in counts:
                df[word] = df.get(word, 0) + 1
        self.idf = {word: math.log(1 + (total - n + 0.5) / (n + 0.5)) for word, n in df.items()}

    def search(self, query, top_k=3, min_score=1.0):
        """
        Rank the sections for a query by BM25.

        ### Args

        - **query** (str): The words to look for
        - **top_k** (int): The most sections to return
        - **min_score** (float): The lowest score a section needs; a section
            without any word of the query never counts

        ### Returns

        - **list[KnowledgeHit]**: The best sections, best first

        """
        words = set(re.findall(r'\w+', (query or '').lower()))
        average = sum(self.lengths) / len(self.lengths) if self.lengths else 0
        hits = []
        for (source, number, text), length, counts in zip(self.sections, self.lengths, self.counts):
            score = 0.0
            for word in words:
                tf = counts.get(word, 0)
                if tf:
                    norm = BM25_K1 * (1 - BM25_B + BM25_B * length / average)
                    score += self.idf[word] * tf * (BM25_K1 + 1) / (tf + norm)
            if score > 0 and score >= min_score:
                hits.append(KnowledgeHit(source, number, round(score, 2), text))
        hits.sort(key=lambda hit: (-hit.score, hit.source, hit.section))
        return hits[:top_k]


def format_hits(hits, max_chars=2000):
    """
    Render hits as numbered sources for the model.

    ### Args

    - **hits** (list[KnowledgeHit]): The sections found
    - **max_chars** (int): The most characters in total; 0 is no limit

    ### Returns

    - **str**: One block per hit, ```[1] vacation.md#2 (score 3.1)``` and its
        text; empty when there are no hits

    """
    text = '\n\n'.join(f'[{i}] {hit.source}#{hit.section} (score {hit.score})\n{hit.text}' for i, hit in enumerate(hits, 1))
    return text[:max_chars] if max_chars else text
