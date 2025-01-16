import socket as s
import json
import hashlib
import time


class CLIENT:
    def __init__(self):
        self.CL_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    def login(self, server_address):
        self.CL_socket.connect(server_address)
        print("Connected to server.")

    def auth_handling(self):
        try:
            packet = json.loads(self.CL_socket.recv(2084).decode("utf-8"))
            if packet.get("type") == 5:
                key = hashlib.sha256(str(self.CL_socket.getsockname()).encode()).hexdigest()
                new_packet = {
                    "type": 5,
                    "content": key
                }
                self.CL_socket.send(json.dumps(new_packet).encode("utf-8"))
                print("Authentication packet sent.")
            else:
                print("Unexpected packet type received.")
        except Exception as e:
            print(f"Error in authentication: {e}")

    def Handle(self):
        while True:
            typeINPUT = int(input("Packet Type [2,3] -> "))
            if typeINPUT == 2:
                target = input("Adresse target -> ")
                command = input("Enter Command -> ")
                packet = {
                    "type": 2,
                    "content": {"command": [f"{command}", f"{target}"]}
                }
                self.CL_socket.send(json.dumps(packet).encode("utf-8"))
                print("Packet send waiting for response...")
                print(self.CL_socket.recv(2048).decode("utf-8"))

            elif typeINPUT == 3:
                print("Packet send waiting for response...")
                packet = {
                    "type": 3,
                    "content": {"command": [f"get_num_of_online"]}
                }
                self.CL_socket.send(json.dumps(packet).encode("utf-8"))
                print(self.CL_socket.recv(2048).decode("utf-8"))

if __name__ == "__main__":
    client = CLIENT()
    server_address = ("127.0.0.1", 15999)
    client.login(server_address)
    client.auth_handling()
    client.Handle()