import typing

import pytest
from lark import Lark


@pytest.fixture
def comment_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="comment", rule="COMMENT")


@pytest.mark.parametrize(
    "text",
    [
        ";",
        ";;",
        "; whatever",
        ";; whatever",
        ";     ",
    ],
)
def test_parse_comment(comment_parser: Lark, text: str):
    comment_parser.parse(text)
