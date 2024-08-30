import socket
from groq import Groq
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)
client_socket, addr = server_socket.accept()
print(f"Connection from {addr} has been established!")
groq_api_key = "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"

def get_llm_response(text):
    client = Groq(api_key=groq_api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    return chat_completion.choices[0].message.content

def send_message(socket, message):
    # Convert message to JSON and then to bytes
    message = json.dumps(message).encode('utf-8')
    message_length = len(message)
    # Send the length of the message first
    socket.sendall(message_length.to_bytes(4, byteorder='big'))
    # Send the actual message
    socket.sendall(message)

def receive_message(socket):
    # First receive the message length
    raw_msglen = recvall(socket, 4)
    if not raw_msglen:
        return None
    msglen = int.from_bytes(raw_msglen, byteorder='big')
    # Now receive the actual message data
    return recvall(socket, msglen)

def recvall(socket, n):
    """Helper function to receive n bytes or return None if EOF is hit"""
    data = bytearray()
    while len(data) < n:
        packet = socket.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

while True:
    data = receive_message(client_socket)
    if not data:
        break
    print(f"Received {data.decode()} from the client")
    data = json.loads(data.decode("utf-8"))
    response = get_llm_response(data["text"])
    response_obj = {
        "client_id": data["client_id"],
        "text": data["text"],
        "response": response
    }
    send_message(client_socket, response_obj)

client_socket.close()
server_socket.close()
