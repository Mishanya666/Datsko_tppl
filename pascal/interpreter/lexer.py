from .token import Token, TokenType


class Lexer:
    def init(self):
        self._position = 0
        self._input = ""
        self._current_char = None

    def initialize(self, s: str):
        self._position = 0
        self._input = s
        self._current_char = self._input[self._position]

    def _advance(self):
        self._position += 1
        if self._position >= len(self._input):
            self._current_char = None
        else:
            self._current_char = self._input[self._position]

    def _skip_whitespace(self):
        while self._current_char and self._current_char.isspace():
            self._advance()

    def _read_number(self):
        result = ""
        while self._current_char and (self._current_char.isdigit() or self._current_char == "."):
            result += self._current_char
            self._advance()
        return result

    def _read_identifier(self):
        result = ""
        while self._current_char and self._current_char.isalpha():
            result += self._current_char
            self._advance()
        if result == "BEGIN":
            return Token(TokenType.BEGIN, "")
        elif result == "END":
            return Token(TokenType.END, "")
        else:
            return Token(TokenType.ID, result)

    def _read_assign(self):
        result = ":"
        while self._current_char:
            if self._current_char.isspace():
                break
            result += self._current_char
            self._advance()
        return Token(TokenType.ASSIGN, result)

    def get_next_token(self):
        self._skip_whitespace()
        if not self._current_char:
            return Token(TokenType.EOF, None)

        if self._current_char.isdigit():
            return Token(TokenType.NUMBER, self._read_number())

        if self._current_char.isalpha():
            return self._read_identifier()

        if self._current_char == "=":
            return self._read_assign()

        raise ValueError(f"Illegal character {self._current_char}")