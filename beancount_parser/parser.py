import json
import pathlib
import typing

from lark import Lark
from lark import Tree

GRAMMAR_FOLDER = pathlib.Path(__file__).parent / "grammar"
BEANCOUNT_GRAMMAR_FILE = GRAMMAR_FOLDER / "beancount.lark"


def make_parser(**options: typing.Any) -> Lark:
    default_options = dict(propagate_positions=True, parser="lalr")
    with open(BEANCOUNT_GRAMMAR_FILE, "rt") as fo:
        return Lark(grammar=fo, **(default_options | options))


def extract_includes(tree: Tree):
    """Extract include statements from the root tree"""
    if tree.data != "start":
        raise ValueError("Expected start")
    for child in tree.children:
        if child is None:
            continue
        if child.data != "statement":
            raise ValueError("Expected statement")
        first_child = child.children[0]
        if not isinstance(first_child, Tree):
            continue
        if first_child.data != "simple_directive":
            continue
        include = first_child.children[0]
        if include.data != "include":
            continue
        yield json.loads(include.children[0].value)


def traverse(
    parser: Lark, bean_file: pathlib.Path
) -> typing.Generator[tuple[pathlib.Path, Tree], None, None]:
    """Traverse a given bean file and follow all its includes, yield (path, parsed_tree) tuples"""
    visited_bean_files: set[pathlib.Path] = set()
    tree = parser.parse(bean_file.read_text())
    includes = extract_includes(tree)
