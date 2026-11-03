"""
Today conductor example for the {{ app_name }} ai agent.

A conductor directs the run. This one makes sure a calendar agent works with
the real date: after the first model answer it adds a call of the tool
```current```, unless the model calls it itself. fundi runs the added call like
any other, through the guards and the sandbox, and asks the model again with
the result. An added call runs only when the agent offers the tool.

An added tool call is more reliable than a hint in the text: a weaker model may
ignore a late system message, an executed call it cannot.

This module is self-contained: it holds only the conductor class. The project
names it by its class path (module:Class) under ```ai.conductors``` in the
config, so it needs no registration and no entry in the app extensions.

```yaml
ai:
  conductors:
    today_call:
      type: {{ app_label }}.core.ai.conductors.today:{{ app_class_name }}AiTodayConductor
      options:
        tool: current
```
"""

from tokeo.core.ai import TokeoAiConductor
from tokeo.core.ai.governor import GOVERNOR_STAGE_ON_ANSWER
from tokeo.core.ai.utils import add_tool_call
from tokeo.core.utils.uid import get_token_hex


class {{ app_class_name }}AiTodayConductor(TokeoAiConductor):
    """
    Add a call of the date tool to the first model answer.

    ```on_answer``` runs after each model call; a mark in ```ctx.turndata```
    under the conductor's own name keeps it to the first one, so it never
    injects twice.

    """

    class Meta:
        """Today conductor meta-data."""

        # tool: the tool that returns the current date
        config_defaults = dict(
            tool='current',
        )

        # the options that hold tool names, checked by the linter
        tool_name_options = ('tool',)

    def on_answer(self, ctx, result):
        """
        Add the date call to the first answer, unless the model made it.

        ### Args

        - **ctx** (TokeoAiContext): The running state
        - **result** (ChatResult): The model answer

        ### Returns

        - **ChatResult|None**: A new answer with the added call, or ```None```

        """
        mark = f'{self.config_name}:today'
        if ctx.turndata.get(mark):
            return None
        ctx.turndata[mark] = True
        tool = self._config('tool', stage=GOVERNOR_STAGE_ON_ANSWER)
        if any(call.name == tool for call in result.tool_calls or []):
            return None
        return add_tool_call(result, tool, get_token_hex(4, 'inj_'))
