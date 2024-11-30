from .token import TokenType, Token
from .ast import BinOp, Constant, UnaryOperation, Variable, Operation
from .parser import Parser

class Executor:
    def init(self):
        self._parser = Parser()
        self._variables = {}

    def execute(self, code: str) -> float:
        trees = self._parser.parse(code)
        for tree in trees:
            self._variables[tree.id.value] = self.evaluate(tree.expr)
        return self._variables

    def evaluate(self, node):
        if isinstance(node, Constant):
            return float(node.token.value)
        elif isinstance(node, Operation):
            return self.handle_operation(node)
        elif isinstance(node, UnaryOperation):
            return self.handle_unary_operation(node)
        elif isinstance(node, Variable):
            return self.handle_variable(node)

    def handle_operation(self, node: Operation) -> float:
        match node.op.value:
            case "+":
                return self.evaluate(node.left) + self.evaluate(node.right)
            case "-":
                return self.evaluate(node.left) - self.evaluate(node.right)
            case "*":
                return self.evaluate(node.left) * self.evaluate(node.right)
            case "/":
                return self.evaluate(node.left) / self.evaluate(node.right)
            case _:
                raise RuntimeError(f"Unsupported operation {node.op.value}")

    def handle_unary_operation(self, node: UnaryOperation) -> float:
        match node.op.value:
            case "+":
                return +self.evaluate(node.expr)
            case "-":
                return -self.evaluate(node.expr)
            case _:
                raise RuntimeError(f"Unsupported unary operator {node.op.value}")

    def handle_variable(self, node: Variable) -> float:
        if node.id.value in self._variables:
            return float(self._variables[node.id.value])
        else:
            raise RuntimeError(f"Variable '{node.id.value}' is not defined")