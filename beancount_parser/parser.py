import pathlib

from lark import Lark

GRAMMAR_FOLDER = pathlib.Path(__file__).parent / "grammar"
BEANCOUNT_GRAMMAR_FILE = GRAMMAR_FOLDER / "beancount.lark"


def make_parser() -> Lark:
    with open(BEANCOUNT_GRAMMAR_FILE, "rt") as fo:
        return Lark(grammar=fo, propagate_positions=True)
