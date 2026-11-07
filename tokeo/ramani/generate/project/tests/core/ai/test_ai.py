"""
Real test cases for the {{ app_name }} ai setup.

Checks the project's own tools, the ```guarded``` agent, and the guard
pipeline against the real shipped configuration (the testing environment
merges ```testing.d/ai.yaml``` over ```base.d/ai.yaml```, pointing the file tools
below ```tmp/tests```). Run from the project root, for example with
```pytest tests/core/ai/test_ai.py```.
"""

import logging
from pathlib import Path

import pytest
from tokeo.core.ai import Invocation, ChatResult, ChatMessage, TraceStep, TokeoAiError, TokeoAiContext
from tokeo.core.ai.guards.confirm import GOVERNOR_CONFIRM_CHANNEL_HOOK, TokeoAiConfirmAnswer
from tokeo.core.utils.date import get_utc_now
from tokeo.core.ai.tool import create_tool_result
from tokeo.core.ai.linter import TokeoAiLinter
from tokeo.core.ai.guards.validate import TokeoAiToolSchemaValidator
from tokeo.core.ai.guards.redact import TokeoAiRegexRedactGuard, TokeoAiRedactGuardError
from {{ app_label }}.core.ai.transformers.truncate import {{ app_class_name }}AiTruncateTransformer
from {{ app_label }}.core.ai.transformers.today import {{ app_class_name }}AiTodayTransformer
from {{ app_label }}.core.ai.transformers.retrieve import {{ app_class_name }}AiRetrieveTransformer
from {{ app_label }}.core.ai.knowledge import KnowledgeIndex
from {{ app_label }}.core.ai.tools.calc import TokeoAiCalcTool
from {{ app_label }}.main import {{ app_class_name }}Test


class {{ app_class_name }}AiTestApp({{ app_class_name }}Test):

    class Meta:
        # set framework extensions
        extensions = [
            'colorlog',
            'tokeo.ext.yaml',
            'tokeo.ext.vault',
            'tokeo.ext.appenv',
            'tokeo.ext.print',
            'tokeo.ext.jinja2',
            'tokeo.ext.appshare',
            'tokeo.ext.ai',
        ]


#: The scratch area of the file tools in the testing environment
#: (testing.d/ai.yaml)
TESTS_DIR = Path('tmp/tests')


@pytest.fixture
def scratch():
    # seed the scratch area and clean up the files a test may create
    TESTS_DIR.mkdir(parents=True, exist_ok=True)
    sample = TESTS_DIR / 'sample.txt'
    sample.write_text('buy milk\n')
    yield TESTS_DIR
    for name in ('sample.txt', 'notes.txt'):
        (TESTS_DIR / name).unlink(missing_ok=True)


def test_{{ app_label }}_ai_config_lints_clean():
    # the shipped ai configuration is sound (types resolve, references exist)
    with {{ app_class_name }}AiTestApp() as app:
        assert TokeoAiLinter(app).lint() == []


def test_{{ app_label }}_ai_tools_exec(scratch):
    # the project tools work when called directly, and the file tools stay
    # strictly below their configured base directory
    with {{ app_class_name }}AiTestApp() as app:
        # calc and read_file hand back a raw value; the date tools and the file
        # writer hand back a ToolResult whose as_str the model would see, so the
        # test reads each according to what the tool returns
        assert app.ai._get_tool('calc').exec(input='2 + 3') == 5
        assert len(app.ai._get_tool('current').exec().value.as_str) == 24  # YYYY-mm-dd HH:MM:SS.MMMZ
        assert app.ai._get_tool('read_file').exec(path='sample.txt') == 'buy milk\n'
        appended = app.ai._get_tool('append_file').exec(text='hello')
        assert appended.value.as_str == 'true' and appended.value.as_data['file'] == 'notes.txt'
        # the date tools take a date-only string as utc, so the calendar step is
        # stable on every machine; clamping shows jan 31 + 1m -> feb 28,
        # jun 8 - 4m -> feb 8, feb 29 + 1y -> feb 28
        assert app.ai._get_tool('add_months').exec(date='2026-01-31', months=1).value.as_str == '2026-02-28'
        assert app.ai._get_tool('add_months').exec(date='2026-06-08', months=-4).value.as_str == '2026-02-08'
        assert app.ai._get_tool('add_years').exec(date='2024-02-29', years=1).value.as_str == '2025-02-28'
        assert (scratch / 'notes.txt').read_text() == 'hello\n'
        with pytest.raises(TokeoAiError, match='escapes the tool base directory'):
            app.ai._get_tool('read_file').exec(path='../../setup.py')
        with pytest.raises(TokeoAiError, match='no such file'):
            app.ai._get_tool('read_file').exec(path='missing.txt')


def test_{{ app_label }}_ai_agent_guarded_runs_tools(scratch):
    # the guarded agent answers through the loop: calculate, tell the time,
    # and read a file, driven by the built-in mock model
    with {{ app_class_name }}AiTestApp() as app:
        assert app.ai.ask('calc 2 + 3', agent='guarded', profile='mock') == 'Done. The tool returned: 5'
        assert app.ai.ask('current', agent='guarded', profile='mock').startswith('Done. The tool returned: 2')
        assert app.ai.ask('read_file sample.txt', agent='guarded', profile='mock') == 'Done. The tool returned: buy milk\n'


def test_{{ app_label }}_ai_trace_records_the_whole_run(scratch):
    # the trace is the run's full, ordered history as a list of steps: each
    # step carries an origin and the object it left in hand. one tool call
    # appears in several steps (one per guard that ran), but they are the same
    # object; the guards refined it in place, so each is an unchanged step
    with {{ app_class_name }}AiTestApp() as app:
        result = app.ai.chat([{'role': 'user', 'content': 'calc 2 + 3'}], agent='guarded', profile='mock')
        assert result.answer.text == 'Done. The tool returned: 5'
        assert all(isinstance(step, TraceStep) for step in result.trace)
        # the conversation turns and the model rounds are on the trace
        messages = [step.object for step in result.trace if isinstance(step.object, ChatMessage)]
        assert any(message.get('role') == 'user' for message in messages)
        assert any(message.get('role') == 'tool' for message in messages)
        # the one tool call: many invocation steps, but a single object
        invocation_steps = [step for step in result.trace if isinstance(step.object, Invocation)]
        distinct = {id(step.object) for step in invocation_steps}
        assert len(distinct) == 1
        invocation = invocation_steps[0].object
        assert invocation.name == 'calc'
        assert invocation.decision == Invocation.ALLOW
        # each guard that ran is an attributable step (the loop tracked the call,
        # then policy/validate/redact/truncate/audit each left their step)
        guard_steps = [step for step in invocation_steps if step.origin is not None and step.is_changed is False]
        assert len(guard_steps) >= 1
        # the trace is chronological: the user turn's step precedes the call's
        objects = [step.object for step in result.trace]
        assert objects.index(messages[0]) < objects.index(invocation)


def test_{{ app_label }}_ai_agent_guarded_denies_writing(scratch):
    # the readonly policy denies the writing tool by name: the call never
    # runs, the loop continues, and the audit guard records the denial
    logs = []
    handler = logging.Handler()
    handler.emit = lambda record: logs.append(record.getMessage())
    with {{ app_class_name }}AiTestApp() as app:
        app.log.backend.addHandler(handler)
        app.log.backend.setLevel(logging.INFO)
        result = app.ai.chat([{'role': 'user', 'content': 'append_file hello'}], agent='guarded', profile='mock')
        assert "denied: tool 'append_file' is not permitted by policy" in result.answer.text
        # the trace records steps; pick the tool call out by the step's object
        invocation_steps = [step for step in result.trace if isinstance(step.object, Invocation)]
        distinct = {id(step.object) for step in invocation_steps}
        assert len(distinct) == 1
        invocation = invocation_steps[0].object
        assert invocation.decision == 'deny'
        # cross-check via the constant: literal and constant must agree
        assert invocation.decision == Invocation.DENY
        assert invocation.result is None
        assert not (scratch / 'notes.txt').exists()
        assert any('ai trace' in message and 'denied' in message for message in logs)


def test_{{ app_label }}_ai_tool_schema_validator_denies_when_strict():
    # strict mode denies a malformed call against the tool's real schema before
    # anything runs (here: the required "input" is missing)
    with {{ app_class_name }}AiTestApp() as app:
        guard = TokeoAiToolSchemaValidator(app)
        # strict comes from the item's options, handed in by _setup
        guard._setup(app, 'tool_schema_validate', {'options': {'strict': True}})
        invocation = Invocation(id='t1', name='calc', arguments={}, parameters=TokeoAiCalcTool.Meta.parameters)
        guard.on_call(None, invocation)
        assert invocation.decision == 'deny'
        assert invocation.decision == Invocation.DENY
        assert "missing required argument 'input'" in invocation.reason


def test_{{ app_label }}_ai_tool_schema_validator_flags_when_not_strict():
    # the default (strict false) only flags a malformed call: the reason is set
    # (so it shows on the trace) and a warning is logged, but the call still runs
    logs = []
    handler = logging.Handler()
    handler.emit = lambda record: logs.append(record.getMessage())
    with {{ app_class_name }}AiTestApp() as app:
        app.log.backend.addHandler(handler)
        app.log.backend.setLevel(logging.WARNING)
        guard = TokeoAiToolSchemaValidator(app)
        # a setup without a config: the guard runs on its class defaults
        guard._setup(app)
        invocation = Invocation(id='t1', name='calc', arguments={}, parameters=TokeoAiCalcTool.Meta.parameters)
        guard.on_call(None, invocation)
        # not denied: the call is allowed to run
        assert invocation.decision == Invocation.ALLOW
        # but flagged: the reason carries the problem, on the trace and in the log
        assert "missing required argument 'input'" in invocation.reason
        assert any("missing required argument 'input'" in line for line in logs)


def test_{{ app_label }}_ai_redact_guard_masks_secrets():
    # the regex redact guard masks secret-looking spans at both tool stages: a
    # result text at on_return, and the call's string arguments at on_call, so a
    # leaked token never reaches history/trace/log
    with {{ app_class_name }}AiTestApp() as app:
        guard = TokeoAiRegexRedactGuard(app)
        # patterns are required (no built-in list); hand them in through _setup
        guard._setup(
            app,
            'regex_redact',
            {
                'options': {
                    'patterns': [
                        r'(?i)\bbearer\s+[A-Za-z0-9._\-]{8,}',
                        r'(?i)\b(?:api[_-]?key|secret|password|token)\b\s*[:=]\s*\S+',
                    ],
                },
            },
        )
        # on_return: a secret in the returned text is masked
        invocation = Invocation(id='t1', name='read_file', arguments={})
        invocation.result = create_tool_result('the page said Bearer abc123DEF456ghi789 here')
        guard.on_return(None, invocation)
        assert 'abc123DEF456ghi789' not in invocation.result.value.as_str
        assert '[redacted]' in invocation.result.value.as_str
        assert 'redacted' in (invocation.reason or '')
        assert invocation.decision == 'allow'
        # on_call: a secret in a string argument is masked in place
        call = Invocation(id='t2', name='read_file', arguments={'q': 'token=swordfish123', 'n': 5})
        guard.on_call(None, call)
        assert 'swordfish123' not in call.arguments['q']
        assert '[redacted]' in call.arguments['q']
        # a non-string argument is left untouched
        assert call.arguments['n'] == 5
        assert call.decision == 'allow'
        assert invocation.decision == Invocation.ALLOW


def test_{{ app_label }}_ai_redact_guard_raises_on_missing_pattern():
    # with no patterns configured the guard must abort the run on the first call
    # that reaches a masking stage, rather than silently mask nothing and let a
    # secret through
    with {{ app_class_name }}AiTestApp() as app:
        guard = TokeoAiRegexRedactGuard(app)
        guard._setup(app)
        invocation = Invocation(id='t1', name='read_file', arguments={})
        invocation.result = create_tool_result('Bearer abc123DEF456ghi789')
        with pytest.raises(TokeoAiRedactGuardError, match='missing or invalid pattern'):
            guard.on_return(None, invocation)


def test_{{ app_label }}_ai_truncate_transformer_cuts_long_results():
    # the project truncate transformer keeps the head of an over-long text and
    # marks the cut, so a big blob cannot overflow the context. it acts at two
    # stages: on_return (a tool result) and on_close (the final answer)
    with {{ app_class_name }}AiTestApp() as app:
        transformer = {{ app_class_name }}AiTruncateTransformer(app)
        transformer._setup(app, 'truncate', dict(options=dict(max_chars=10)))
        # on_return cuts the tool result text and notes the cut on reason
        invocation = Invocation(id='t1', name='read_file', arguments={})
        invocation.result = create_tool_result('x' * 50)
        transformer.on_return(None, invocation)
        assert invocation.result.value.as_str == 'x' * 10 + '... [truncated 40 chars]'
        assert 'truncated 40 chars' in (invocation.reason or '')
        # on_close cuts the run's final answer text
        result = ChatResult(text='y' * 50)
        transformer.on_close(None, result)
        assert result.text == 'y' * 10 + '... [truncated 40 chars]'


def test_{{ app_label }}_ai_today_transformer_puts_the_date_in_front_once():
    # the input pipeline: at on_prompt the transformer inserts today's date as
    # the first message; a second model call of the same run adds nothing
    with {{ app_class_name }}AiTestApp() as app:
        transformer = {{ app_class_name }}AiTodayTransformer(app)
        transformer._setup(app, 'today_prompt', dict(options={}))
        ctx = TokeoAiContext(messages=[{'role': 'user', 'content': 'welcher tag ist heute'}])
        transformer.on_prompt(ctx)
        transformer.on_prompt(ctx)
        assert [m['role'] for m in ctx.messages] == ['system', 'user']
        assert ctx.messages[0]['content'] == f'Today is {get_utc_now().date().isoformat()} (UTC).'


def test_{{ app_label }}_ai_today_conductor_adds_the_date_call(scratch):
    # the mock answers without a tool, the conductor adds a call of current
    # to that first answer; the model then answers with the real date
    with {{ app_class_name }}AiTestApp() as app:
        result = app.ai.chat([{'role': 'user', 'content': 'welcher tag ist heute'}], agent='dated', profile='mock')
    calls = [step.object for step in result.trace if isinstance(step.object, Invocation)]
    assert {(call.name, call.id[:4]) for call in calls} == {('current', 'inj_')}
    assert get_utc_now().date().isoformat() in result.answer.text


def test_{{ app_label }}_ai_a_confirm_note_makes_the_word_filter_judge_anew(scratch):
    # careful asks a person before append_file. the first answer is no_retry
    # with a note, the word filter reads it and denies the same call; the
    # person confirms that decision with yes, so the call never runs
    first = TokeoAiConfirmAnswer('no_retry', by='human', note='deny: world')
    answers = iter([first, TokeoAiConfirmAnswer('yes', by='human')])

    def answer_confirm(app, request):
        return next(answers)

    with {{ app_class_name }}AiTestApp(hooks=[(GOVERNOR_CONFIRM_CHANNEL_HOOK, answer_confirm)]) as app:
        result = app.ai.chat([{'role': 'user', 'content': 'append_file hello world'}], agent='careful', profile='mock')
    asked = [(c['answer'], c['previous_decision'], c['previous_reason']) for c in result.confirmations]
    assert asked == [('no_retry', 'allow', None), ('yes', 'deny', "contains 'world'")]
    assert "denied: contains 'world'" in result.answer.text
    assert not (scratch / 'notes.txt').exists()


def test_{{ app_label }}_ai_the_word_filter_denies_its_configured_words(scratch):
    # without any note the configured word password is denied, no question
    # changes that; the default of confirm (no) keeps the no
    with {{ app_class_name }}AiTestApp() as app:
        result = app.ai.chat([{'role': 'user', 'content': 'append_file my password'}], agent='careful', profile='mock')
    assert "contains 'password'" in result.answer.text
    assert not (scratch / 'notes.txt').exists()


def test_{{ app_label }}_ai_knowledge_index_ranks_sections_with_sources():
    # BM25 over the sections of docs/knowledge: the vacation section ranks
    # first, its heading stays with its text, a word nowhere finds nothing
    index = KnowledgeIndex.of('docs/knowledge')
    hits = index.search('how many vacation days per year')
    assert (hits[0].source, hits[0].section) == ('vacation.md', 1)
    assert hits[0].text.startswith('# Vacation\nEvery employee gets 30 vacation days')
    assert [hit.score for hit in hits] == sorted((hit.score for hit in hits), reverse=True)
    assert index.search('xylophone') == []


def test_{{ app_label }}_ai_knowledge_index_is_built_again_after_a_change(scratch):
    # the index lives in memory and is built again when a file changes
    knowledge_dir = scratch / 'knowledge'
    knowledge_dir.mkdir(exist_ok=True)
    (knowledge_dir / 'a.md').write_text('apples are green')
    try:
        assert KnowledgeIndex.of(str(knowledge_dir)).search('bananas', min_score=0) == []
        (knowledge_dir / 'a.md').write_text('apples are green\n\nbananas are yellow')
        hits = KnowledgeIndex.of(str(knowledge_dir)).search('bananas', min_score=0)
        assert [(hit.source, hit.section) for hit in hits] == [('a.md', 2)]
    finally:
        (knowledge_dir / 'a.md').unlink()
        knowledge_dir.rmdir()


def test_{{ app_label }}_ai_retrieve_transformer_puts_sources_before_the_question():
    # the input pipeline as a small RAG: the fitting sections go as a system
    # message right before the question, numbered with their sources
    with {{ app_class_name }}AiTestApp() as app:
        transformer = {{ app_class_name }}AiRetrieveTransformer(app)
        transformer._setup(app, 'retrieve', dict(options=dict(base_dir='docs/knowledge', top_k=2)))
        ctx = TokeoAiContext(messages=[{'role': 'user', 'content': 'which hotel price per night'}])
        transformer.on_prompt(ctx)
        transformer.on_prompt(ctx)
        assert [m['role'] for m in ctx.messages] == ['system', 'user']
        assert '[1] travel.md#2' in ctx.messages[0]['content']
        assert '150 euros per night' in ctx.messages[0]['content']
        # without a fitting section the conversation stays as it is
        ctx = TokeoAiContext(messages=[{'role': 'user', 'content': 'xylophone'}])
        transformer.on_prompt(ctx)
        assert [m['role'] for m in ctx.messages] == ['user']


def test_{{ app_label }}_ai_search_docs_tool_answers_with_sources():
    # the model asks for the sections itself: the tool call passes the guards
    # of informed and the answer names the source
    with {{ app_class_name }}AiTestApp() as app:
        result = app.ai.chat([{'role': 'user', 'content': 'search_docs hotel per night'}], agent='informed', profile='mock')
    assert '[1] travel.md#2' in result.answer.text
    assert '150 euros per night' in result.answer.text
