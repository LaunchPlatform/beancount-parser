import pathlib

import pytest
from lark import Lark

from beancount_parser.parser import extract_includes
from beancount_parser.parser import make_parser
from beancount_parser.parser import traverse


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


@pytest.mark.parametrize(
    "folder, expected",
    [
        ("nested", ["main.bean", "a/file0.bean", "a/b/file1.bean"]),
        ("circular", ["main.bean", "file0.bean", "file1.bean"]),
    ],
)
def test_traverse(
    parser: Lark, fixtures_folder: pathlib.Path, folder: str, expected: list[str]
):
    bean_file = fixtures_folder / "traverse" / folder / "main.bean"
    assert frozenset(
        str(bean_path.relative_to(bean_file.parent).as_posix())
        for bean_path, _ in traverse(parser, bean_file)
    ) == frozenset(expected)
