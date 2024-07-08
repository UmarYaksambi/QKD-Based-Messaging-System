# QKD-Based Inter-Device Payment and Messaging

This project demonstrates the implementation of a secure communication protocol using Quantum Key Distribution (QKD) for inter-device payment and messaging applications. The simulation involves two systems, Alice (sender) and Bob (receiver), that use QKD to securely generate a shared secret key over a network. This key is then used to encrypt and decrypt messages, ensuring confidentiality and integrity.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Files](#files)
- [How to Run](#how-to-run)
  - [Step 1: Start Bob's Script](#step-1-start-bobs-script)
  - [Step 2: Start Alice's Script](#step-2-start-alices-script)
  - [Configuration](#configuration)
- [Project Structure](#project-structure)
  - [QKD Functions](#qkd-functions)
  - [Alice's Script](#alices-script)
  - [Bob's Script](#bobs-script)
- [Example Output](#example-output)
  - [Alice's Output](#alices-output)
  - [Bob's Output](#bobs-output)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features
- **Quantum Key Distribution (QKD):** Implements the BB84 protocol for secure key exchange.
- **Error Correction and Privacy Amplification:** Ensures a high level of security by correcting errors and reducing information an eavesdropper could gain.
- **XOR Encryption:** Uses a simple XOR encryption and decryption.
- **Network Communication:** Facilitates secure communication between two devices over a network.
- **GUI Application:** Includes threaded messaging, graphical message display, and secure data transmission using QKD.

## Prerequisites
- Python 3.x
- Required Python libraries: `numpy`, `socket`, `customtkinter`

## Installation
Install the required libraries using:
```bash
pip install numpy socket customtkinter
```

## Files
- `QKD.py`: Contains the QKD protocol functions.
- `Alice.py`: Script to run terminal Alice's side of the QKD and communication.
- `Bob.py`: Script to run terminal Bob's side of the QKD and communication.
- `Server-Application-Integrated.py`: Script to run GUI based server side of QKD and communication.
- `Client-Application-Integrated.py`: Script to run GUI based client side of QKD and communication.
- `README.md`: Project documentation.

## Installation

### Step 1: Clone the repository:
```bash
$ git clone https://github.com/umaryaksambi/QKD-Based-Messaging-System.git
$ cd QKD-Based-Messaging-System
```

### Step 2: Install dependencies:

```bash
pip install numpy socket customtkinter
```

### Step 3: Run the application:
Run the following command on Bob's system (replace `127.0.0.1` with common networks IP address for inter device communication if needed):

-Start the terminal-based messaging:
-Bob acts as the receiver. - Alice acts as the sender. Run the following command on Alice's system:
```bash
$ python Alice.py
$ python Bob.py
```

- Launch the GUI application:
```bash
$ python Server-Application-Integrated.py
$ python Client-Application-Integrated.py
```

### Configuration
By default, the scripts are configured to run on localhost (`127.0.0.1`). To run on different devices, update the `host` variable in both `alice.py` and `bob.py` to the appropriate IP addresses.

## Project Structure

### QKD Functions
The `qkd.py` file contains the core QKD protocol functions:

- `prepare_and_send_bits(num_bits)`: Generates random bits and bases for Alice.
- `eavesdrop_and_measure(alice_bits, alice_bases, num_bits, eavesdropping_probability)`: Simulates eavesdropping by an attacker.
- `measure_bits(alice_bits, alice_bases, eaves_bits, eaves_bases, intercepted, num_bits)`: Simulates Bob's measurement of Alice's bits.
- `sift_bits(alice_bases, bob_bases, alice_bits, bob_bits)`: Performs sifting to generate the shared key.
- `detect_eavesdropping(sifted_alice_bits, sifted_bob_bits)`: Detects potential eavesdropping by comparing a subset of the bits.
- `error_correction(sifted_alice_bits, sifted_bob_bits)`: Corrects errors in Bob's key.
- `privacy_amplification(sifted_alice_bits, corrected_bob_bits)`: Amplifies privacy to reduce information an eavesdropper could gain.

### Alice's Script

The `alice.py` script performs the following steps:
1. Generates random bits and bases.
2. Connects to Bob's system over a network.
3. Sends the generated bases and bits to Bob.
4. Receives Bob's bases and bits.
5. Performs sifting, error detection, and key generation.
6. Encrypts a message or payment details using the generated key.
7. Sends the encrypted message or payment details to Bob.

```python
import socket
import numpy as np
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# QKD Functions
from qkd import *

def alice_send_qkd(host, port):
    num_bits = 1000
    alice_bits, alice_bases = prepare_and_send_bits(num_bits)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Send the bases and bits to Bob
        s.sendall(alice_bases.tobytes())
        s.sendall(alice_bits.tobytes())
        print("Alice sent bases and bits to Bob.")

        # Receive Bob's bases and bits
        bob_bases = np.frombuffer(s.recv(num_bits), dtype=np.int8)
        bob_bits = np.frombuffer(s.recv(num_bits), dtype=np.int8)
        print("Alice received bases and bits from Bob.")
        
        # Perform sifting
        sifted_alice_bits, sifted_bob_bits = sift_bits(alice_bases, bob_bases, alice_bits, bob_bits)
        
        # Detect eavesdropping
        error_rate = detect_eavesdropping(sifted_alice_bits, sifted_bob_bits)
        print(f"Error Rate: {error_rate:.2%}")
        
        if error_rate > 0.1:
            print("Eavesdropping detected. Terminating the process.")
            return
        else:
            print("No significant eavesdropping detected. Key exchange successful.")
        
        # Error correction and privacy amplification
        corrected_bob_bits = error_correction(sifted_alice_bits, sifted_bob_bits)
        final_alice_key, final_bob_key = privacy_amplification(sifted_alice_bits, corrected_bob_bits)
        
        # Convert the key to a 16-byte AES key
        key_length = min(len(final_alice_key), 16)  # AES-128 requires a 16-byte key
        aes_key = bytes(final_alice_key[:key_length])
        
        # Simulate messaging
        message = "Hello, Bob! This is Alice."
        print(f"Alice's original message: {message}")
        
        encrypted_message = encrypt_message(aes_key, message)
        print(f"Encrypted message: {encrypted_message.hex()}")
        
        # Send the encrypted message to Bob
        s.sendall(encrypted_message)
        print("Alice sent the encrypted message to Bob.")

def main():
    host = '127.0.0.1'  # Bob's IP address
    port = 65432        # Port to connect to Bob
    alice_send_qkd(host, port)

if __name__ == "__main__":
    main()
```

### Bob's Script

The `bob.py` script performs the following steps:
1. Listens for Alice's connection.
2. Receives bases and bits from Alice.
3. Generates random bases and measures Alice's bits.
4. Sends its bases and measured bits back to Alice.
5. Receives the encrypted message or payment details from Alice.
6. Decrypts the received message or payment details using the generated key.

```python
import socket
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# QKD Functions
from qkd import *

def bob_receive_qkd(host, port):
    num_bits = 1000
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Bob is listening for Alice...")
        
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            
            # Receive the bases and bits from Alice
            alice_bases = np.frombuffer(conn.recv(num_bits), dtype=np.int8)
            alice_bits = np.frombuffer(conn.recv(num_bits), dtype=np.int8)
            
            # Bob generates his own bases and measures Alice's bits
            bob_bases = np.random.randint(2, size=num_bits)
            bob_bits = measure_bits(alice_bits, alice_bases, [], [], [], num_bits)[0]
            
            # Send Bob's bases and bits back to Alice
            conn.sendall(bob_bases.tobytes())
            conn.sendall(bob_bits.tobytes())
            print("Bob sent his bases and measured bits back to Alice.")
            
            # Receive the encrypted message from Alice
            encrypted_message = conn.recv(1024)
            print(f"Encrypted message received: {encrypted_message.hex()}")
            
            # Assuming Alice and Bob perform the same error correction and privacy amplification
            # These steps should be the same as in Alice's script
            sifted_alice_bits, sifted_bob_bits = sift_bits(alice_bases, bob_bases, alice_bits, bob_bits)
            corrected_bob_bits = error_correction(sifted_alice_bits, sifted_bob_bits)
            final_alice_key, final_bob_key = privacy_amplification(sifted_alice_bits, corrected_bob_bits)


            
            # Convert the key to a 16-byte AES key
            key_length = min(len(final_bob_key), 16)  # AES-128 requires a 16-byte key
            aes_key = bytes(final_bob_key[:key_length])
            
            # Decrypt the message
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(f"Bob's decrypted message: {decrypted_message}")

def main():
    host = '127.0.0.1'  # Bob's IP address
    port = 65432        # Port to listen on
    bob_receive_qkd(host, port)

if __name__ == "__main__":
    main()
```

## Example Output

### Alice's Output
```
Alice sent bases and bits to Bob.
Alice received bases and bits from Bob.
Error Rate: 0.00%
No significant eavesdropping detected. Key exchange successful.
Alice's original message: Hello, Bob! This is Alice.
Encrypted message: <hexadecimal representation>
Alice sent the encrypted message to Bob.
```

### Bob's Output
```
Bob is listening for Alice...
Connected by ('127.0.0.1', <port>)
Bob sent his bases and measured bits back to Alice.
Encrypted message received: <hexadecimal representation>
Bob's decrypted message: Hello, Bob! This is Alice.
```

## Future Enhancements
- **Support Additional QKD Protocols:** Implement other QKD protocols such as E91.
- **Graphical User Interface (GUI):** Develop a GUI to visualize the key distribution process, error rates, and encrypted messages.
- **Performance Metrics:** Measure and display metrics such as key generation rate and encryption/decryption time.
- **Integration with Real-world Applications:** Extend the simulation to integrate with real-world payment and messaging systems.

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [BB84 Protocol](https://en.wikipedia.org/wiki/BB84)
- [Python Sockets](https://docs.python.org/3/library/socket.html)
- [PyCryptodome](https://www.pycryptodome.org/)

---
