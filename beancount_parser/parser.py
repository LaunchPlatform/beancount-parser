import pathlib
import typing

from lark import Lark

GRAMMAR_FOLDER = pathlib.Path(__file__).parent / "grammar"
BEANCOUNT_GRAMMAR_FILE = GRAMMAR_FOLDER / "beancount.lark"


def make_parser(**options: typing.Any) -> Lark:
    default_options = dict(propagate_positions=True, parser="lalr")
    with open(BEANCOUNT_GRAMMAR_FILE, "rt") as fo:
        return Lark(grammar=fo, **(default_options | options))
