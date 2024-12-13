from notation.exceptions import InsufficientOperandsError, InvalidTokenError, InvalidExpressionError

class PrefixToInfix:
    def __init__(self):
        self.expression_stack = []

    def _is_operator(self, token):
        return token in "+-*/"

    def _apply_operator(self, operator, operand1, operand2):
        return f"({operand1} {operator} {operand2})"

    def convert(self, expression: str) -> str:
        tokens = expression.split()

        for token in reversed(tokens):
            if token.isdigit():
                self.expression_stack.append(token)
            elif self._is_operator(token):
                if len(self.expression_stack) < 2:
                    raise InsufficientOperandsError("Недостаточно операндов для оператора")

                op1 = self.expression_stack.pop()
                op2 = self.expression_stack.pop()

                result = self._apply_operator(token, op1, op2)
                self.expression_stack.append(result)
            else:
                raise InvalidTokenError("Некорректный токен в выражении")

        if len(self.expression_stack) != 1:
            raise InvalidExpressionError("Неправильное количество операндов или операторов")

        return self.expression_stack.pop()
