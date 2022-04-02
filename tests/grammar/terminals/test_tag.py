import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters


@pytest.fixture
def tag_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="tag", rule="TAG")


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
