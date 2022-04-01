import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def plugin_parser() -> Lark:
    return Lark(
        """
    start: plugin
    %import .plugin.plugin
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


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
