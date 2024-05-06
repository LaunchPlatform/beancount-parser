import pathlib

import pytest
from lark import Lark

from beancount_parser.helpers import collect_entries
from beancount_parser.parser import make_parser


@pytest.fixture
def parser() -> Lark:
    return make_parser()


def test_collect_entries(parser: Lark, fixtures_folder: pathlib.Path):
    bean_file = fixtures_folder / "simple.bean"
    tree = parser.parse(bean_file.read_text())
    entries, tail_comments = collect_entries(tree)
    # TODO: assert more stuff here
    assert len(entries) == 12
    assert len(tail_comments) == 1
