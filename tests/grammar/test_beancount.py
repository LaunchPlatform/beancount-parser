from textwrap import dedent

import pytest
from lark import Lark

from beancount_parser.parser import make_parser


@pytest.fixture
def parser() -> Lark:
    return make_parser()


@pytest.mark.parametrize(
    "text",
    [
        "1970-01-01 open Assets:MyBank USD",
    ],
)
def test_parse(parser: Lark, text: str):
    result = parser.parse(text)
    assert result
