# import socket
# import threading
# import sys
# import json

# if len(sys.argv) != 2:
#     print("Missing argument")
#     sys.exit(1)

# client_id = int(sys.argv[1])

# with open('input.txt', 'r') as file:
#     lines = file.readlines()

# Listening = True

# def listen_for_server_messages(client_socket):
#     #"""Function to listen for incoming messages from the server."""
#     while Listening:
#         try:
#             # Receive the length of the incoming message
#             raw_msglen = recvall(client_socket, 4)
#             if not raw_msglen:
#                 print("Server closed the connection.")
#                 break
#             msglen = int.from_bytes(raw_msglen, byteorder='big')

#             # Now, receive the entire message based on its length
#             data = recvall(client_socket, msglen)
#             print(f"Received from server: {data.decode()}")
#         except ConnectionResetError:
#             print("Connection was closed by the server.")
#             break
#     client_socket.close()

# def recvall(socket, n):
# #    """Helper function to receive n bytes or return None if EOF is hit."""
#     data = bytearray()
#     while len(data) < n:
#         packet = socket.recv(n - len(data))
#         if not packet:
#             return None
#         data.extend(packet)
#     return data

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('localhost', 12345))
# listen_thread = threading.Thread(target=listen_for_server_messages, args=(client_socket,))
# listen_thread.start()

# responses = []

# def send_rec_prompt(text):
#     text_obj = {
#         "client_id": client_id,
#         "text": text
#     }
#     message = json.dumps(text_obj).encode("utf-8")
#     # Send the length of the message first
#     client_socket.sendall(len(message).to_bytes(4, byteorder='big'))
#     # Then send the actual message
#     client_socket.sendall(message)

# for line in lines:
#     send_rec_prompt(line.strip())

# Listening = False
# client_socket.close()
# print(responses)

import socket
import threading
import sys
import json

if len(sys.argv) != 2:
    print("Missing argument")
    sys.exit(1)

client_id = int(sys.argv[1])

with open('input.txt', 'r') as file:
    lines = file.readlines()

# Initialize Listening flag as a threading Event for thread-safe signaling
Listening = threading.Event()
Listening.set()

def listen_for_server_messages(client_socket):
    while Listening.is_set():
        try:
            # Receive the length of the incoming message
            raw_msglen = recvall(client_socket, 4)
            if not raw_msglen:
                print("Server closed the connection.")
                break
            msglen = int.from_bytes(raw_msglen, byteorder='big')

            # Now, receive the entire message based on its length
            data = recvall(client_socket, msglen)
            print(f"Received from server: {data.decode()}")
        except ConnectionResetError:
            print("Connection was closed by the server.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    client_socket.close()

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

# Create a socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Start the listening thread
listen_thread = threading.Thread(target=listen_for_server_messages, args=(client_socket,))
listen_thread.start()

responses = []

def send_rec_prompt(text):
    text_obj = {
        "client_id": client_id,
        "text": text
    }
    message = json.dumps(text_obj).encode("utf-8")
    # Send the length of the message first
    client_socket.sendall(len(message).to_bytes(4, byteorder='big'))
    # Then send the actual message
    client_socket.sendall(message)

# Send all lines from the input file to the server
for line in lines:
    send_rec_prompt(line.strip())


listen_thread.join()  # Wait for the listening thread to terminate

# Close the socket once the thread has safely stopped
client_socket.close()
print(responses)
