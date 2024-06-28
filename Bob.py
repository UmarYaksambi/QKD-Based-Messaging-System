# Hello, This is BOB. 
# For Demonstraion Porpose Im The Server Connecting Alice & Me(Bob) 
# This Connection Taking Place Btwn Alice & Me(Bob) Simulates 
# Interconnection Through Optical FIber And Like Wise

import socket
import numpy as np

def eavesdrop_and_measure(alice_bits, alice_bases, num_bits, eavesdropping_probability):
    eaves_bits = np.zeros(num_bits, dtype=int)
    eaves_bases = np.random.randint(0, 2, num_bits)
    intercepted = (np.random.rand(num_bits) < eavesdropping_probability)
    
    for i in range(num_bits):
        if intercepted[i]:
            if eaves_bases[i] == alice_bases[i]:
                eaves_bits[i] = alice_bits[i]
            else:
                eaves_bits[i] = np.random.randint(0, 2)
                
    return eaves_bits, eaves_bases, intercepted

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(1)
    
    print('Server is waiting for connection...')
    conn, addr = server_socket.accept()
    print('Connected by', addr)

    num_bits = 64
    eavesdropping_probability = 0.7
    alice_bits = np.random.randint(0, 2, num_bits, dtype=np.uint8)
    alice_bases = np.random.randint(0, 2, num_bits, dtype=np.uint8)
    
    eaves_bits, eaves_bases, intercepted = eavesdrop_and_measure(alice_bits, alice_bases, num_bits, eavesdropping_probability)
    
    # Send the number of bits first
    conn.sendall(num_bits.to_bytes(4, byteorder='big'))
    
    # Send Alice's bits and bases to the client (Bob)
    conn.sendall(alice_bits.tobytes())
    conn.sendall(alice_bases.tobytes())
    
    while True:
        message = conn.recv(1024).decode('utf-8')
        if message.lower() == 'quit':
            print("Alice has ended the connection.")
            break
        print("Alice: ", message)
        
        response = input("Enter a message to send to Alice (or type 'quit' to end): ")
        if response.lower() == 'quit':
            conn.sendall(response.encode('utf-8'))
            break
        conn.sendall(response.encode('utf-8'))

    # Close the connection
    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
