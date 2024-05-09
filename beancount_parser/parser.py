import glob
import json
import logging
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


def extract_includes(tree: Tree) -> typing.Generator[tuple[str, int], None, None]:
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
        yield json.loads(include.children[0].value), first_child.meta.line


def traverse(
    parser: Lark, bean_file: pathlib.Path, root_dir: pathlib.Path | None = None
) -> typing.Generator[tuple[pathlib.Path, Tree], None, None]:
    """Traverse a given bean file and follow all its includes, yield (path, parsed_tree) tuples"""
    logger = logging.getLogger(__name__)
    visited_bean_files: set[pathlib.Path] = set()

    if root_dir is None:
        root_dir = bean_file.parent.absolute()
    pending_files = [bean_file.absolute()]

    while pending_files:
        current_file = pending_files.pop(0)
        visited_bean_files.add(current_file)
        tree = parser.parse(current_file.read_text())
        yield current_file, tree
        includes = extract_includes(tree)
        for include, lineno in includes:
            logger.info(
                "Process include at %s:%s with path value %s",
                current_file,
                lineno,
                include,
            )
            target_file = current_file.parent / include
            for matched_file in glob.glob(str(target_file)):
                matched_file = pathlib.Path(matched_file).resolve().absolute()
                if root_dir not in matched_file.parents:
                    logger.warning(
                        "Matched file %s is not a sub-path of root %s, ignored",
                        matched_file,
                        root_dir,
                    )
                    # ensure include cannot go above the root folder, to avoid any potential security risk
                    continue
                if matched_file in visited_bean_files:
                    continue
                pending_files.append(matched_file)
