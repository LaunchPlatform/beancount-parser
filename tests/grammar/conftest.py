import pathlib
import typing
from textwrap import dedent

import pytest
from lark import Lark

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def grammar_folder() -> pathlib.Path:
    return GRAMMAR_FOLDER


@pytest.fixture
def make_parser(grammar_folder: pathlib.Path) -> typing.Callable:
    def _make_parser(module: str, rule: str, ignore_spaces: bool = False):
        ignore_statement = ""
        if ignore_spaces:
            ignore_statement = "\n".join(
                ["%import common.WS_INLINE", "%ignore WS_INLINE"]
            )
        return Lark(
            dedent(
                f"""\
        start: {rule}
        %import .{module}.{rule}
        {ignore_statement}
        """
            ),
            import_paths=[grammar_folder],
            parser="lalr",
            debug=True,
        )

    return _make_parser
