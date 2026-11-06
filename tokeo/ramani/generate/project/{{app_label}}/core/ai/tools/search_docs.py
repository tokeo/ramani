"""
Search docs tool for the {{ app_name }} ai agent.

The model asks for knowledge itself: the tool ranks the sections of the text
files below ```base_dir``` for a query (BM25, ```core/ai/knowledge.py```) and
returns the best ones with their sources. Unlike the retrieve transformer, the
retrieval is a tool call, so it passes the guards and the sandbox like any
other: redact can mask, truncate can cut, the trace records the hits.

This module is self-contained: it holds only the tool class. The project names
it by its class path (module:Class) under ```ai.tools``` in the config, so it needs
no registration and no entry in the app extensions.
"""

from tokeo.core.ai import TokeoAiTool
from tokeo.core.ai.tool import create_tool_result
from {{ app_label }}.core.ai.knowledge import KnowledgeIndex, format_hits


class TokeoAiSearchDocsTool(TokeoAiTool):
    """
    Tool that returns the sections of the knowledge files that fit a query.

    The value is the list of hits (source, section, score, text); the model
    sees them as numbered sources.

    """

    class Meta:
        """Tool meta-data sent to the model."""

        # Short description the model sees
        description = 'search the project documents and return the best sections with their sources'

        # JSON-schema object describing the arguments
        parameters = dict(
            type='object',
            properties=dict(query=dict(type='string', description='the words to look for')),
            required=['query'],
        )

        # the defaults of the options
        config_defaults = dict(
            # the directory of the knowledge files
            base_dir='docs/knowledge',
            # the max count of sections
            top_k=3,
            # the lowest BM25 score a section needs
            min_score=1.0,
        )

    def exec(self, query):
        """
        Return the best sections for the query.

        ### Args

        - **query** (str): The words to look for

        ### Returns

        - **ToolResult**: The hits as data; as_str numbers them with their
            sources, or says that nothing was found

        """
        index = KnowledgeIndex.of(self._config('base_dir'))
        hits = index.search(query, top_k=self._config('top_k'), min_score=self._config('min_score'))
        data = [dict(source=hit.source, section=hit.section, score=hit.score, text=hit.text) for hit in hits]
        return create_tool_result(data, as_str=format_hits(hits, max_chars=0) or 'nothing found')
