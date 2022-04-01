from beancount_parser.parser import make_parser


def test_parsexx():
    parser = make_parser()
    result = parser.parse("; this is fine")
    assert result


def test_parse():
    parser = make_parser()
    result = parser.parse(
        '2022-03-31 * "Foobar"\n Assets:MyBank 12.34 USD ; this is fine'
    )
    assert result
