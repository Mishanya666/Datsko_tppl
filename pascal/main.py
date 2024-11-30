from interpreter import Token, TokenType
from interpreter import Executor

with open('./tests/input.txt', 'r') as f:
    text = f.read()

print(text)

evaluator = Executor()
result = evaluator.execute("BEGIN x:=3/-2; y:=x END.")
print(result)