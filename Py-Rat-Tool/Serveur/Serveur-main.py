try:
    import socket as s
    import threading
    import json
    import datetime
    import hashlib
    import os
    import sqlite3
except ImportError:
    try:
        os.system("pip install -r Dependencies.txt")
    except:
        print("Please make sure all dependencies are correctly installed\n-->pip install -r Dependencies.txt")

""" 
Data Demo:

{
type": 1
"content": {bla bla bla},   
}

1 => Result from client
2 => Command from Admin 
3 => Ask from client
4 => Error
5 => Authentification protocol
6 => Command from server to client
"""

class SERVER:
    def __init__(self, ip: str, port: int):
        self.ADDR = (ip, port)
        self.KNOW_USER = self.open_db()
        self.CONNECTED_USER = {}

    def open_db(self):
        with open("data/user_database.json", "r") as db:
            return json.loads(db.read())

    def add_to_db(self, client_address, client_socket, is_admin):
        self.KNOW_USER.update({client_address: [client_socket, is_admin]})

    def add_to_userlist(self, client_address, client_socket, is_admin):
        self.CONNECTED_USER.update({client_address: [client_socket, is_admin]})

    def remove_from_userlist(self, client_address):
        self.CONNECTED_USER.pop(client_address)

    def is_in_db(self, client_address):
        return client_address in self.KNOW_USER

    def log(self, msg):
        log_filename = f"LogDir\\LogFile_{datetime.date.today()}.txt"
        with open(log_filename, "a") as file:
            log = f"[{datetime.datetime.now()}] - {msg}\n"
            file.write(log)
            print(log.removesuffix("\n"))

    def boot(self):
        self.log("Booting Initialization...")
        self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.server_socket.bind(self.ADDR)
        self.server_socket.listen(4)
        self.log("Server booted and is now listening...")

    def authHash(self, client_addr):
        return hashlib.sha256(str(client_addr).encode()).hexdigest()

    def make_json_serializable(self, obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    def execute_command_on(self, client_address, command):
        client_socket = self.CONNECTED_USER[client_address][0]
        packet = {
            "type": 6,
            "content": command
        }
        client_socket.send(json.dumps(packet).encode("utf-8"))
        return client_socket.recv(2048).decode("utf-8")

    def analyze(self, data, client_socket: s.socket, client_addr, is_admin: bool):
        try:
            data = json.loads(data)
            type = data.get("type")
            if type == 1:
                self.log(f"Data Type 1 received from {client_addr}")
            elif type == 2:
                if is_admin:
                    target = data.get("content")[1]
                    result = self.execute_command_on(target, data.get("content"))
                    self.log(f"Packet received from (admin){client_addr}")
                    packet = {
                        "type": 1,
                        "content": result
                    }
                    client_socket.send(json.dumps(packet).encode('utf-8'))
                    self.log(f"Response from {target} to (admin) {client_addr}")
                else:
                    error = {
                    "type": 4,
                    "content": {"error": "402 - Access Denied"}
                     }
                    client_socket.send(json.dumps(error, default=self.make_json_serializable).encode("utf-8"))
            elif type == 3:
                self.log(f"Data Type 3 received from {client_addr}")
            else:
                error = {
                    "type": 4,
                    "content": {"error": "401 - Wrong Request Type"}
                }
                client_socket.send(json.dumps(error, default=self.make_json_serializable).encode("utf-8"))
                self.log(f"Error 401 sent to {client_addr}")
        except Exception as e:
            self.log(f"Error analyzing data from {client_addr}: {e}")

    def verify_is_admin(self, client_socket: s.socket, client_addr):
        try:
            packet = {"type": 5, "content": ""}
            client_socket.send(json.dumps(packet).encode('utf-8'))
            response = client_socket.recv(8064).decode("utf-8")
            response = json.loads(response)
            key = self.authHash(client_addr)
            return response.get('content') == key
        except Exception as e:
            self.log(f"Admin verification failed for {client_addr}: {e}")
            return False

    def handle_client(self, client_socket: s.socket, client_addr):
        try:
            if not self.is_in_db(client_addr):
                is_admin = self.verify_is_admin(client_socket, client_addr)
            else:
                is_admin = self.KNOW_USER[client_addr][1]
            role = "admin" if is_admin else "client"
            self.log(f"New connection: {role} -> {client_addr}")
            self.add_to_userlist(client_addr, client_socket, is_admin)
            while True:
                data = client_socket.recv(8064).decode("utf-8")
                if not data:
                    break
                self.analyze(data, client_socket, client_addr, is_admin)
        except ConnectionResetError:
            self.log(f"Connection reset by {client_addr}")
        except Exception as e:
            self.log(f"Error with client {client_addr}: {e}")
        finally:
            client_socket.close()
            self.log(f"Connection closed for {client_addr}")

    def close_connection(self, client_socket, client_address):
        client_socket.close()
        self.remove_from_userlist(client_address)

    def stop(self):
        self.server_socket.close()
        self.log("Server shuttingdown...")

    def run(self):
        try:
            self.boot()
            while True:
                client_socket, client_addr = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_addr))
                client_thread.start()
        except Exception as e:
            self.log(f"Server error: {e}")
        finally:
            self.stop()

if __name__ == '__main__':
    SERVER("127.0.0.1", 15999).run()