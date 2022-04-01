from textwrap import dedent

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def event_parser() -> Lark:
    return Lark(
        """
    start: event
    %import .event.event
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        '2022-03-31 event "employer" "Launch Platform LLC"',
        '2022-03-31 event "location" "San Francisco"; this is a comment',
        dedent(
            """\
        2022-03-31 event "location" "San Francisco"
            foo: "bar"
            egg: #spam
        """
        ),
    ],
)
def test_parse_event(event_parser: Lark, text: str):
    event_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        'event "foo" "this account looks good"',
        '2022-03-31 event "foo"',
    ],
)
def test_parse_bad_event(event_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        event_parser.parse(text)
