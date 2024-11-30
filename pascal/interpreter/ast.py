from .token import Token, TokenType

class Node:
    pass

class Number(Node):
    def init(self, token: Token):
        self.token = token

    def str(self):
        return f"{self.__class__.__name__} {self.token}"

class BinOp(Node):
    def init(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def str(self):
        return f"{self.__class__.__name__} {self.op.value}({self.left}, {self.right})"

class UnaryOperation(Node):
    def init(self, op: Token, expr: Node):
        self.expr = expr
        self.op = op

    def str(self):
        return f"{self.__class__.__name__} {self.op.value}({self.expr})"

class Variable(Node):
    def init(self, id: Token, expr: Node):
        self.id = id
        self.expr = expr

    def str(self):
        return f"{self.__class__.__name__} {self.id} = {self.expr}"

class Assign(Node):
    def init(self, variable: Variable, value: Node):
        self.variable = variable
        self.value = value

    def str(self):
        return f"{self.__class__.__name__} {self.variable} := {self.value}"

class Block(Node):
    def init(self, statements):
        self.statements = statements

    def str(self):
        return f"{self.__class__.__name__}({', '.join(str(s) for s in self.statements)})"
class Constant(Node):
    def init(self, token: Token):
        self.token = token

    def str(self):
        return f"{self.__class__.__name__} {self.token}"

class Operation:
    def init(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator