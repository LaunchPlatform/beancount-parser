from textwrap import dedent

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def note_parser() -> Lark:
    return Lark(
        """
    start: note
    %import .note.note
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


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
