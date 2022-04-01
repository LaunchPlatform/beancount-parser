import typing
from textwrap import dedent

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def note_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="note", rule="note", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        '2022-03-31 note Assets "this account looks good"',
        '2022-03-31 note Assets "this account looks good" ; this is a comment',
        dedent(
            """\
        2022-03-31 note Assets "this account looks good"
            foo: "bar"
            egg: #spam
        """
        ),
    ],
)
def test_parse_note(note_parser: Lark, text: str):
    note_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        'note Assets "this account looks good"',
        "2022-03-31 note Assets",
    ],
)
def test_parse_bad_note(note_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        note_parser.parse(text)
