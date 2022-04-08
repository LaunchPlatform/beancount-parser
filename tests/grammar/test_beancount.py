from textwrap import dedent

import pytest
from lark import Lark

from beancount_parser.parser import make_parser


@pytest.fixture
def parser() -> Lark:
    return make_parser()


@pytest.mark.parametrize(
    "text",
    [
        dedent(
            """\
    1970-01-01 commodity USD
    1970-01-01 open Assets:MyBank USD
    
    option "foo" "bar"
    include "2022.bean"
    plugin "beancount.module"
    
    """
        ),
        dedent(
            """\
    2022-03-31 * "Foobar"
        Assets:MyBank 12.34 USD ; this is fine
    """
        ),
        dedent(
            """\
    2022-03-31 * "Foobar"
        Assets:MyBank 12.34 USD ; this is fine"""
        ),
        dedent(
            """\
    1970-01-01 commodity USD
    1970-01-01 open Assets:MyBank USD
    1970-01-01 note Assets:MyBank "this is my first bank account"
    1970-01-01 open Assets:My2ndBank USD,BTC
    1970-01-01 close Assets:My2ndBank
    1970-01-01 price BTC 100.0 USD
    1970-01-01 commodity USD
    1970-01-01 custom "string val" 123.45 USD TRUE FALSE 2022-04-01 Assets:Bank
    
       ; comment
    ; comment
    1970-01-01 event "job" "working from home"

    * org
    
    2022-03-31
        Assets:MyBank 12.34 USD
        
    2022-03-31 "foo" "bar"
        Assets:MyBank 12.34 USD
        
    ** org2
    
    2022-03-31 * "Foobar"
        document: "foobar.pdf" ; my doc
        document-2: "egg-spam.pdf"
        Assets:MyBank 12.34 USD ; this is fine
            document: "invoice.pdf"
            source: "invoice.pdf"

    """
        ),
        dedent(
            """\
        ;; -*- mode: org; mode: beancount; -*-
        
        """
        ),
        "",
    ],
)
def test_parse(parser: Lark, text: str):
    parser.parse(text)
