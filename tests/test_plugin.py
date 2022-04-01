import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def plugin_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="plugin", rule="plugin", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        'plugin "beancount.plugin"',
        'plugin "beancount.plugin" "config"',
        'plugin "beancount.plugin" "config" ; this is a comment',
    ],
)
def test_parse_plugin(plugin_parser, text: str):
    plugin_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        'plugin beancount.plugin "value"',
        "plugin 'beancount.plugin' 'value'",
    ],
)
def test_parse_bad_plugin(plugin_parser, text: str):
    with pytest.raises(UnexpectedInput):
        plugin_parser.parse(text)
