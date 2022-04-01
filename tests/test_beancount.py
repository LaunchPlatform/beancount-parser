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
        dedent(
            """\
    2022-03-31 * "Foobar"
        Assets:MyBank 12.34 USD ; this is fine
    """
        )
    ],
)
def test_parse(parser: Lark, text: str):
    result = parser.parse(text)
    assert result
