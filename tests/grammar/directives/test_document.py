import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def document_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="beancount", rule="document", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        '2022-03-31 document Assets "/path/to/the/file.pdf"',
    ],
)
def test_parse_document(document_parser: Lark, text: str):
    document_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        'document Assets "this account looks good"',
        "2022-03-31 document Assets",
    ],
)
def test_parse_bad_document(document_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        document_parser.parse(text)
