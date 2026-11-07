"""
Retrieve transformer example for the {{ app_name }} ai agent.

A small RAG in the input pipeline: at ```on_prompt``` the transformer ranks the
sections of the text files below ```base_dir``` for the user's question (BM25,
```core/ai/knowledge.py```) and puts the best ones, numbered with their
sources, as a system message in front of the question. The model answers from
them and names the source. The trace records the message, so a run shows which
sections it used and why.

This module is self-contained: it holds only the transformer class. The
project names it by its class path (module:Class) under ```ai.transformers``` in
the config, so it needs no registration and no entry in the app extensions.

```yaml
ai:
  transformers:
    retrieve:
      type: {{ app_label }}.core.ai.transformers.retrieve:{{ app_class_name }}AiRetrieveTransformer
      options:
        base_dir: docs/knowledge
        max_sections: 3
```
"""

from tokeo.core.ai import TokeoAiTransformer
from tokeo.core.ai.governor import GOVERNOR_STAGE_ON_PROMPT
from {{ app_label }}.core.ai.knowledge import KnowledgeIndex, format_hits


class {{ app_class_name }}AiRetrieveTransformer(TokeoAiTransformer):
    """
    Put the sections that fit the question in front of it, once per run.

    ```on_prompt``` runs before each model call; a mark in ```ctx.turndata```
    under the transformer's own name keeps it to the first one. Without a hit
    the conversation stays as it is.

    """

    class Meta:
        """Retrieve transformer meta-data."""

        # the defaults of the options
        config_defaults = dict(
            # the directory of the knowledge files
            base_dir='docs/knowledge',
            # the max count of sections
            max_sections=3,
            # the lowest BM25 score a section needs
            min_score=1.0,
            # the max characters of context, 0 means unlimited
            max_chars=2000,
            # the system message, "{sources}" are the numbered sections
            text='Answer from these sources and name the source by its number:\n\n{sources}',
        )

    def on_prompt(self, ctx):
        """
        Insert the best sections before the last user message.

        ### Args

        - **ctx** (TokeoAiContext): The running state; ```ctx.messages``` is
            the conversation about to be sent, changed in place

        """
        mark = f'{self.config_name}:retrieve'
        if ctx.turndata.get(mark):
            return
        ctx.turndata[mark] = True
        stage = GOVERNOR_STAGE_ON_PROMPT
        users = [i for i, message in enumerate(ctx.messages) if message.get('role') == 'user']
        if not users:
            return
        question = ctx.messages[users[-1]].get('content') or ''
        index = KnowledgeIndex.get_index(self._config('base_dir', stage=stage))
        hits = index.search(
            question,
            max_sections=self._config('max_sections', stage=stage),
            min_score=self._config('min_score', stage=stage),
        )
        if not hits:
            return
        sources = format_hits(hits, max_chars=self._config('max_chars', stage=stage))
        ctx.messages.insert(users[-1], dict(role='system', content=self._config('text', stage=stage).format(sources=sources)))
