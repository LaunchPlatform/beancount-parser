import typing

import pytest
from lark import Lark


@pytest.fixture
def org_anchor_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="org_anchor", rule="ORG_ANCHOR")


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
def test_parse_org_anchor(org_anchor_parser: Lark, text: str):
    org_anchor_parser.parse(text)
