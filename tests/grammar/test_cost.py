import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def cost_parser(make_parser: typing.Callable) -> Lark:
    import logging
    from lark import logger

    logger.setLevel(level=logging.DEBUG)
    return make_parser(module="beancount", rule="cost", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        "{ 12.34 USD }",
        "{{ 12.34 USD }}",
        "{ 12.34 # 56.78 USD }",
        "{ 12.34 USD, 2024-01-01 }",
    ],
)
def test_parse_cost(cost_parser: Lark, text: str):
    cost_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "12.34 USD",
    ],
)
def test_parse_bad_cost(cost_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        cost_parser.parse(text)
