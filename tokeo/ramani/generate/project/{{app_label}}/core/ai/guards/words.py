"""
Word filter guard example for the {{ app_name }} ai agent.

A policy guard that denies a tool call whose arguments contain a listed word.
It also reads the notes of confirm answers (```ctx.notes```): a note
```deny: word, other``` adds words. So a person who answers ```no_retry``` with
such a note gets a new judgment of the same call, and the next confirm shows
the new decision.

Put it before the confirm guard on the agent, so confirm sees its decision.

This module is self-contained: it holds only the guard class. The project names
it by its class path (module:Class) under ```ai.guards``` in the config, so it
needs no registration and no entry in the app extensions.

```yaml
ai:
  guards:
    words:
      type: {{ app_label }}.core.ai.guards.words:{{ app_class_name }}AiWordFilterGuard
      options:
        words: [password]
        note_prefix: 'deny:'
```
"""

import json

from tokeo.core.ai import Invocation
from tokeo.core.ai.governor import GOVERNOR_STAGE_ON_CALL
from tokeo.core.ai.guards.policy import TokeoAiPolicyGuard


class {{ app_class_name }}AiWordFilterGuard(TokeoAiPolicyGuard):
    """
    Deny a call whose arguments contain a word of the options or the notes.

    The words match case-insensitively anywhere in the arguments as JSON. A
    denial is soft: ```decision``` becomes ```deny``` with the words as reason.

    """

    class Meta:
        """Word filter guard meta-data."""

        # words: always denied. note_prefix: a note starting with it adds the
        # comma-separated words after it
        config_defaults = dict(
            words=[],
            note_prefix='deny:',
        )

    def on_call(self, ctx, invocation):
        """
        Deny the call when its arguments contain a listed word.

        ### Args

        - **ctx** (TokeoAiContext): The running state; ```ctx.notes``` holds
            the notes of confirm answers, also from earlier runs
        - **invocation** (Invocation): The tool call to check

        """
        words = list(self._config('words', stage=GOVERNOR_STAGE_ON_CALL) or [])
        prefix = self._config('note_prefix', stage=GOVERNOR_STAGE_ON_CALL)
        size = len(prefix)
        for record in ctx.notes:
            note = (record.get('note') or '').strip()
            if note.lower().startswith(prefix):
                words += [word.strip() for word in note[size:].split(',') if word.strip()]
        text = json.dumps(invocation.arguments, ensure_ascii=False).lower()
        hits = [word for word in words if word.lower() in text]
        if hits:
            invocation.decision = Invocation.DENY
            invocation.reason = f'contains {", ".join(repr(word) for word in hits)}'
