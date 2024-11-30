from .token import TokenType
from .lexer import Lexer
from .ast import BinOp, Number, UnaryOperation, Assign, Block
class Parser:
    def init(self, lexer: Lexer):
        self._lexer = lexer
        self._current_token = None

    def __consume(self, token_type):
        if self._current_token.type == token_type:
            self._current_token = self._lexer.next()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self._current_token}")

    def __expression(self):
        """Парсинг выражений"""
        left = self.__term()
        while self._current_token.type == TokenType.OPERATOR:
            operator = self._current_token.value
            self.__consume(TokenType.OPERATOR)
            right = self.__term()
            left = (operator, left, right)
        return left

    def __term(self):
        left = self.__factor()
        while self._current_token.type == TokenType.OPERATOR and self._current_token.value in ["*", "/"]:
            operator = self._current_token
            self.__consume(TokenType.OPERATOR)
            right = self.__factor()
            left = (operator.value, left, right)
        return left

    def __factor(self):
        token = self._current_token
        if token.type == TokenType.NUMBER:
            self.__consume(TokenType.NUMBER)
            return ("NUMBER", token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.__consume(TokenType.IDENTIFIER)
            return ("IDENTIFIER", token.value)
        elif token.type == TokenType.LPAREN:
            self.__consume(TokenType.LPAREN)
            expr = self.__expression()
            self.__consume(TokenType.RPAREN)
            return expr
        else:
            raise SyntaxError(f"Expected NUMBER, IDENTIFIER, or LPAREN, got {token}")

    def __statement(self):
        if self._current_token.type == TokenType.IDENTIFIER:
            var_name = self._current_token.value
            self.__consume(TokenType.IDENTIFIER)
            self.__consume(TokenType.ASSIGN)
            expr_value = self.__expression()
            return ("ASSIGN", var_name, expr_value)
        elif self._current_token.type == TokenType.BEGIN:
            return self.__compound_statement()
        elif self._current_token.type == TokenType.END:
            self.__consume(TokenType.END)
            return ("END",)
        else:
            raise SyntaxError(f"Invalid statement: {self._current_token}")

    def __compound_statement(self):
        self.__consume(TokenType.BEGIN)
        statements = []
        while self._current_token.type != TokenType.END:
            statements.append(self.__statement())
            if self._current_token.type == TokenType.SEMI:
                self.__consume(TokenType.SEMI)
        self.__consume(TokenType.END)
        return Block(statements)

    def eval(self, s: str):
        self._lexer.init(s)
        self._current_token = self._lexer.next()
        return self.__compound_statement()