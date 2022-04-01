import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def tag_parser() -> Lark:
    return Lark(
        """
    start: TAG
    %import .tag.TAG
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "#abc",
        "#a123",
        "#this-is-fine",
    ],
)
def test_parse_tag(tag_parser: Lark, text: str):
    tag_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    ["@123", "#", "abc"],
)
def test_parse_bad_tag(tag_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        tag_parser.parse(text)
