"""
Today transformer example for the {{ app_name }} ai agent.

An example of the input pipeline: a transformer at ```on_prompt``` enriches the
conversation before the model sees it. This one puts today's date in front as a
system message, once per run, so the model need not guess the date.

The same stage takes any enrichment of the prompt: a retrieved document, a
shortened history, a rewritten request. Requests from outside (mail, grpc, a
web page) that call ```app.ai.ask``` run through the same stages.

This module is self-contained: it holds only the transformer class. The
project names it by its class path (module:Class) under ```ai.transformers``` in
the config, so it needs no registration and no entry in the app extensions.

```yaml
ai:
  transformers:
    today_prompt:
      type: {{ app_label }}.core.ai.transformers.today:{{ app_class_name }}AiTodayTransformer
      options:
        text: 'Today is {date} (UTC).'
```
"""

from tokeo.core.ai import TokeoAiTransformer
from tokeo.core.ai.governor import GOVERNOR_STAGE_ON_PROMPT
from tokeo.core.utils.date import get_utc_now


class {{ app_class_name }}AiTodayTransformer(TokeoAiTransformer):
    """
    Put today's date in front of the conversation, once per run.

    ```on_prompt``` runs before each model call; a mark in ```ctx.turndata```
    under the transformer's own name keeps it to the first one.

    """

    class Meta:
        """Today transformer meta-data."""

        # the defaults of the options
        config_defaults = dict(
            # the system message, "{date}" is today as YYYY-MM-DD (UTC)
            text='Today is {date} (UTC).',
        )

    def on_prompt(self, ctx):
        """
        Insert the date as the first message on the first model call.

        ### Args

        - **ctx** (TokeoAiContext): The running state; ```ctx.messages``` is
            the conversation about to be sent, changed in place

        """
        mark = f'{self.config_name}:today'
        if ctx.turndata.get(mark):
            return
        ctx.turndata[mark] = True
        text = self._config('text', stage=GOVERNOR_STAGE_ON_PROMPT).format(date=get_utc_now().date().isoformat())
        ctx.messages.insert(0, dict(role='system', content=text))
