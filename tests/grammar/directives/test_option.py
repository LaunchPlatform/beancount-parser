import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def option_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="beancount", rule="option", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        'option "key" "value"',
    ],
)
def test_parse_option(option_parser, text: str):
    option_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        'option "key"',
        'option key "value"',
        "option 'key' 'value'",
    ],
)
def test_parse_bad_option(option_parser, text: str):
    with pytest.raises(UnexpectedInput):
        option_parser.parse(text)
