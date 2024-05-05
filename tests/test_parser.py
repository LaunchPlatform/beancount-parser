import pathlib

import pytest
from lark import Lark

from beancount_parser.parser import extract_includes
from beancount_parser.parser import make_parser


@pytest.fixture
def parser() -> Lark:
    return make_parser()


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "includes.bean",
            [
                "foo.bean",
                "bar.bean",
                "2024/*.bean",
            ],
        )
    ],
)
def test_extract_includes(
    parser: Lark, fixtures_folder: pathlib.Path, filename: str, expected: list[str]
):
    bean_file = fixtures_folder / filename
    tree = parser.parse(bean_file.read_text())
    assert frozenset(extract_includes(tree)) == frozenset(expected)
