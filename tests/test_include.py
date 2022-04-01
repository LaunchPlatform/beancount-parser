import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def include_parser() -> Lark:
    return Lark(
        """
    start: include
    %import .include.include
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        'include "/path/to/file.bean"',
        'include "/path/to/file.bean" ; this is a comment',
    ],
)
def test_parse_include(include_parser: Lark, text: str):
    include_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        'INCLUDE "/path/to/file.bean"',
        "include '/path/to/file.bean'" "include /path/to/file.bean",
    ],
)
def test_parse_bad_include(include_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        include_parser.parse(text)
