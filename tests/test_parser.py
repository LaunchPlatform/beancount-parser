from beancount_parser.parser import make_parser


def test_parse():
    parser = make_parser()
    result = parser.parse("2022-03-31")
    assert result
