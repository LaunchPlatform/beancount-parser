import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters


@pytest.fixture
def link_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="link", rule="LINK", ignore_spaces=True)


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
