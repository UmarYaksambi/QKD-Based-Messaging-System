# QKD-Based Inter-Device Payment and Messaging

This project demonstrates the implementation of a secure communication protocol using Quantum Key Distribution (QKD) for inter-device payment and messaging applications. The simulation involves two systems, Alice (sender) and Bob (receiver), that use QKD to securely generate a shared secret key over a network. This key is then used to encrypt and decrypt messages, ensuring confidentiality and integrity.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Files](#files)
- [Installation](#installation)
  - [Step 1: Clone the repository](#step-1-clone-the-repository)
  - [Step 2: Install dependencies](#step-2-install-dependencies)
  - [Step 3: Run the application](#step-3-run-the-application)
  - [Configuration](#configuration)
- [Project Structure](#project-structure)
  - [QKD Functions](#qkd-functions)
  - [Alice's Script](#alices-script)
  - [Bob's Script](#bobs-script)
- [Example Output](#example-output)
  - [Alice's Output](#alices-output)
  - [Bob's Output](#bobs-output)
- [Future Enhancements](#future-enhancements)
- [Important Notes](#important-notes)
- [Further Exploration](#further-exploration)
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
$ pip install numpy socket customtkinter
```

### Step 3: Run the application:
- Start the terminal-based messaging:
`Alice acts as the sender.`` Bob acts as the receiver. `
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

### Bob's Script

The `bob.py` script performs the following steps:
1. Listens for Alice's connection.
2. Receives bases and bits from Alice.
3. Generates random bases and measures Alice's bits.
4. Sends its bases and measured bits back to Alice.
5. Receives the encrypted message or payment details from Alice.
6. Decrypts the received message or payment details using the generated key.

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
- **Performance Metrics:** Measure and display metrics such as key generation rate and encryption/decryption time.
- **Integration with Real-world Applications:** Extend the simulation to integrate with real-world payment and messaging systems.

## Important Notes:
- This is a work in progress! The core functionalities demonstrate the concepts of QKD-based messaging. There may be limitations and potential bugs. We recommend using it for educational purposes only.
-Security in real-world scenarios can be much more complex. This is a simplified simulation for educational purposes.

## Further Exploration:
- Feel free to explore the code and play around with the different functionalities.
- You can find the server-side code and potentially other scripts (like QKD simulation) in this repository for a more comprehensive understanding of the entire application.
- We hope this client-side application provides a glimpse into the world of secure communication using QKD. Remember, secure messaging is always a good thing!

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [BB84 Protocol](https://en.wikipedia.org/wiki/BB84)
- [Python Sockets](https://docs.python.org/3/library/socket.html)
- [How Quantum Key Distribution Works (BB84 & E91)](https://youtu.be/V3WzH2up7Os?si=6b-gD5h0mJ-jZQnb)

---
