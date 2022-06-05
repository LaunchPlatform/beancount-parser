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
        "Assets:A",
        "Assets:2",
        "Assets:Ab",
        "Assets:AA",
        "Assets:银行",
        "Assets:A银行",
        "Assets:Banks:AMEX",
        "Assets:Banks:WellsFargo",
        "Assets:Banks:Wells-Fargo",
        "Assets:Banks:Chase",
        "Expenses:Housing",
        "Expenses:Travel",
        "Liabilities:CreditCard",
        "Income:Contracting",
        "Income:ProjectNumber8",
        "Equity:My1stHouse",
        "Foobar:Eggs:Spam",
    ],
)
def test_parse_account(account_parser: Lark, text: str):
    account_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "Assets",
        "Expenses",
        "Income",
        "Liabilities",
        "Foobar",
        "assets:bank",
        "Assets:bank",
        ":Assets",
        "Assets:",
        "Assets::Banks:AMEX",
        'USD',
    ],
)
def test_parse_bad_account(account_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        account_parser.parse(text)
