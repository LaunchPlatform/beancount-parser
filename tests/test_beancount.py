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
    1970-01-01 commodity USD
    1970-01-01 open Assets:MyBank USD
    
    option "foo" "bar"
    include "2022.bean"
    plugin "beancount.module"
    
    """
        ),
        dedent(
            """\
    2022-03-31 * "Foobar"
        Assets:MyBank 12.34 USD ; this is fine
    """
        ),
        dedent(
            """\
    1970-01-01 commodity USD
    1970-01-01 open Assets:MyBank USD

    2022-03-31 * "Foobar"
        Assets:MyBank 12.34 USD ; this is fine


    """
        ),
    ],
)
def test_parse(parser: Lark, text: str):
    result = parser.parse(text)
    assert result
