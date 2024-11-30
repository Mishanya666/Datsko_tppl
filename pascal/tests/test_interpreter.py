import pytest
from interpreter import Executor
from interpreter import Token, TokenType
from interpreter import ast


@pytest.fixture(scope="function")
def executor():
    return Executor()


class TestExecutor:
    @pytest.mark.parametrize(
        "string,result",
        [("BEGIN x:=2+2; END.", {"x": 4.0}),
         ("BEGIN x:=2+2; y:=3+3 END.", {"x": 4.0, "y": 6}),
         ("BEGIN x:=2+2; y:=x+3; END.", {"x": 4.0, "y": 7}),
         ("BEGIN x:=2+2; x :=x+3 END.", {"x": 7.0}),
         ("BEGIN x:=2+2; BEGIN y:=x+3; z:=y+3 END; z:=z-x END.", {"x": 4.0, "y": 7.0, "z": 6.0}),
         ("BEGIN x:=2*2; y:=(x+6)/2; END.", {"x": 4.0, "y": 5.0}),
         ("BEGIN x:=-4; y:=(x+6)/2; END.", {"x": -4.0, "y": 1.0}),
         ("BEGIN x:=+4; y:=(x+6)/2; END.", {"x": 4.0, "y": 5.0})]
    )
    def test_constructs(self, string, result, executor):
        assert executor.execute(string) == result

    def test_invalid_begin_end(self, executor):
        with pytest.raises(SyntaxError):
            executor.execute("BEGIN x:=3;.")

    def test_missing_dot_error(self, executor):
        with pytest.raises(SyntaxError):
            executor.execute("BEGIN x:=3; END")

    def test_invalid_operator(self, executor):
        with pytest.raises(SyntaxError):
            executor.execute("BEGIN x :=/3; y:=x END.")

    def test_invalid_assignment(self, executor):
        with pytest.raises(SyntaxError):
            executor.execute("BEGIN x:s=3; y:=x END.")

    def test_ast_print(self):
        n1 = ast.Number(Token(TokenType.NUMBER, "2"))
        n2 = ast.Number(Token(TokenType.NUMBER, "3"))
        assert str(n1) == "Number Token: TokenType.NUMBER, 2"
        assert str(ast.BinOp(n1, Token(TokenType.OPERATOR, "+"),
                             n2)) == "BinOp +(Number Token: TokenType.NUMBER, 2, Number Token: TokenType.NUMBER, 3)"
        assert str(ast.UnaryOp(Token(TokenType.OPERATOR, "-"), n2)) == "UnaryOp -(Number Token: TokenType.NUMBER, 3))"
        assert str(ast.Variable(Token(TokenType.ID, "n"),
                                n1)) == "Variable Token: TokenType.ID, n = Number Token: TokenType.NUMBER, 2"