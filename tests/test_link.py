import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def link_parser() -> Lark:
    return Lark(
        """
    start: LINK
    %import .link.LINK
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "^abc",
        "^a123",
        "^this-is-fine",
    ],
)
def test_parse_link(link_parser: Lark, text: str):
    link_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    ["@123", "#", "abc"],
)
def test_parse_link_tag(link_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        link_parser.parse(text)
