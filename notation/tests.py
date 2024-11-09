import pytest
from main import PrefixToInfix

@pytest.fixture
def prefixtoinfix():
    return PrefixToInfix()


class TestPrefixToInfix:

    def test_simple_expression(self, prefixtoinfix):
        assert prefixtoinfix.convert("+ - 13 4 55") == "((13 - 4) + 55)"

    def test_nested_expression(self, prefixtoinfix):
        assert prefixtoinfix.convert("+ 2 * 2 - 2 1") == "(2 + (2 * (2 - 1)))"

    def test_multiple_operators(self, prefixtoinfix):
        assert prefixtoinfix.convert("+ + 10 20 30") == "((10 + 20) + 30)"

    def test_not_enough_operands(self, prefixtoinfix):
        assert prefixtoinfix.convert("- - 1 2") == "Недостаточно операндов для оператора"

    def test_complex_expression(self, prefixtoinfix):
        assert prefixtoinfix.convert("/ + 3 10 * + 2 3 - 3 5") == "((3 + 10) / ((2 + 3) * (3 - 5)))"

    def test_empty_expression(self, prefixtoinfix):
        assert prefixtoinfix.convert("") == "Неправильное количество операндов или операторов"

    def test_invalid_token(self, prefixtoinfix):
        assert prefixtoinfix.convert("+ 3 a 5") == "Некорректный токен в выражении"
