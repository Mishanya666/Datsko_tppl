from enum import Enum, auto


class TokenType(Enum):
    BEGIN = "BEGIN"
    END = "END"
    ID = "ID"
    IDENTIFIER = "IDENTIFIER"
    PLUS = "+"
    MINUS = "-"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    LPAREN = "("
    RPAREN = ")"
    DOT = "."
    ASSIGN = ":="
    SEMI = "SEMI"
    NUMBER = "NUMBER"
    EOF = "EOF"
    OPERATOR = "OPERATOR"



class Token():
    def __init__(self, type_: TokenType, value: str):
        self.type_ = type_
        self.value = value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.type_}, {self.value})"