import socket
import numpy as np

def recv_all(sock, num_bytes):
    data = bytearray()
    while len(data) < num_bytes:
        packet = sock.recv(num_bytes - len(data))
        if not packet:
            raise ConnectionError("Socket connection closed prematurely")
        data.extend(packet)
    return data

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    
    # Receive the number of bits first
    num_bits = int.from_bytes(recv_all(client_socket, 4), byteorder='big')
    
    # Receive Alice's bits and bases
    alice_bits = np.frombuffer(recv_all(client_socket, num_bits), dtype=np.uint8)
    alice_bases = np.frombuffer(recv_all(client_socket, num_bits), dtype=np.uint8)
    
    # Ensure the received data is of the expected size
    if len(alice_bits) != num_bits or len(alice_bases) != num_bits:
        print("Received data size does not match the expected number of bits.")
        client_socket.close()
        return
    
    # Bob chooses his bases
    bob_bases = np.random.randint(0, 2, num_bits)
    
    # Measure the bits based on Bob's bases
    bob_bits = np.zeros(num_bits, dtype=int)
    for i in range(num_bits):
        if bob_bases[i] == alice_bases[i]:
            bob_bits[i] = alice_bits[i]
        else:
            bob_bits[i] = np.random.randint(0, 2)
    
    # For demonstration, we will print the results
    print("Alice's bits: \n", alice_bits)
    print("Alice's bases: \n", alice_bases)
    print("Bob's bases: \n", bob_bases)
    print("Bob's bits: \n", bob_bits)
    
    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()
