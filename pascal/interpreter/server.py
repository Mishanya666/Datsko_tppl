import socket
from .executor import Interpreter, Parser


def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(2)

        while True:
            print(f"Wait for new connection...")
            conn, addr = sock.accept()
            print(f"Connected {addr}")

            while True:
                message = conn.recv(1024)

                if message == b"":
                    break

                if message == b"exit":
                    conn.send(b"Googbye!")
                    break

                try:
                    if message.startswith(b"@"):
                        parser = Parser()
                        result = parser.eval(message[1:].decode())
                    else:
                        interp = Interpreter()
                        result = interp.eval(message.decode())

                    conn.send(str(result).encode())
                except (SyntaxError, RuntimeError) as e:
                    conn.send(b"error: " + str(e).encode())
