import typing

import pytest
from lark import Lark


@pytest.fixture
def section_header_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="section_header", rule="SECTION_HEADER")


@pytest.mark.parametrize(
    "text",
    [
        "*",
        "**",
        "* whatever",
        "*whatever",
        "*     ",
    ],
)
def test_parse_section_header(section_header_parser: Lark, text: str):
    section_header_parser.parse(text)
