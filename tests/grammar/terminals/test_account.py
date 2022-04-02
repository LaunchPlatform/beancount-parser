import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters


@pytest.fixture
def account_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="account", rule="ACCOUNT")


@pytest.mark.parametrize(
    "text",
    [
        "Assets",
        "Assets:A",
        "Assets:2",
        "Assets:Ab",
        "Assets:AA",
        "Assets:Banks:AMEX",
        "Assets:Banks:WellsFargo",
        "Assets:Banks:Wells-Fargo",
        "Assets:Banks:Chase",
        "Expenses",
        "Expenses:Housing",
        "Expenses:Travel",
        "Liabilities",
        "Liabilities:CreditCard",
        "Income",
        "Income:Contracting",
        "Income:ProjectNumber8",
        "Equity:My1stHouse",
    ],
)
def test_parse_account(account_parser: Lark, text: str):
    account_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "Foobar",
        "assets:bank",
        "Assets:bank",
        ":Assets",
        "Assets:",
        "Assets::Banks:AMEX",
    ],
)
def test_parse_bad_account(account_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        account_parser.parse(text)
