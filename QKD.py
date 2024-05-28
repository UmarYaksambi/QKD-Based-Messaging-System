from numpy import random, zeros
import matplotlib.pyplot as plt

def main():
    num_bits = 1000
    eavesdropping_probability = 0.4
    
    alice_bits, alice_bases = prepare_and_send_bits(num_bits)
    eaves_bits, eaves_bases, intercepted = eavesdrop_and_measure(alice_bits, alice_bases, num_bits, eavesdropping_probability)
    bob_bits, bob_bases = measure_bits(alice_bits, alice_bases, eaves_bits, intercepted, num_bits)
    sifted_alice_bits, sifted_bob_bits = sift_bits(alice_bases, bob_bases, alice_bits, bob_bits)

    error_rate = detect_eavesdropping(sifted_alice_bits, sifted_bob_bits)
    print(f"Error Rate: {error_rate:.2%}")

    if error_rate > 0.1:  # Threshold for eavesdropping detection
        print("Eavesdropping detected. Terminating the process.")
    else:
        print("No significant eavesdropping detected. Key exchange successful.")
        print(f"Sifted Key: {sifted_alice_bits}")

    # Simulate multiple runs and collect error rates
    error_rates = []
    for _ in range(10):
        # Repeat the main simulation and collect error rates
        error_rate = detect_eavesdropping(sifted_alice_bits, sifted_bob_bits)
        error_rates.append(error_rate)

    plot_error_rate(error_rates)


def prepare_and_send_bits(num_bits):
    alice_bits = random.randint(0, 2, num_bits)
    alice_bases = random.randint(0, 2, num_bits)
    return alice_bits, alice_bases


def eavesdrop_and_measure(alice_bits, alice_bases, num_bits, eavesdropping_probability):
    eaves_bits = zeros(num_bits, dtype=int)
    eaves_bases = random.randint(0, 2, num_bits)
    intercepted = (random.rand(num_bits) < eavesdropping_probability)
    
    for i in range(num_bits):
        if intercepted[i]:
            if eaves_bases[i] == alice_bases[i]:
                eaves_bits[i] = alice_bits[i]
            else:
                eaves_bits[i] = random.randint(0, 2)
                
    return eaves_bits, eaves_bases, intercepted


def measure_bits(alice_bits, alice_bases, eaves_bits, intercepted, num_bits):
    bob_bases = random.randint(0, 2, num_bits)
    bob_bits = zeros(num_bits, dtype=int)
    
    for i in range(num_bits):
        if intercepted[i]:
            photon = eaves_bits[i]
        else:
            photon = alice_bits[i]
            
        if alice_bases[i] == bob_bases[i]:
            bob_bits[i] = photon
        else:
            bob_bits[i] = random.randint(0, 2)
    
    return bob_bits, bob_bases


def sift_bits(alice_bases, bob_bases, alice_bits, bob_bits):
    print("Alice bases shape:", alice_bases.shape)
    print("Bob bases shape:", bob_bases.shape)
    
    matches = (alice_bases == bob_bases)
    sifted_alice_bits = alice_bits[matches]
    sifted_bob_bits = bob_bits[matches]
    
    return sifted_alice_bits, sifted_bob_bits


def detect_eavesdropping(sifted_alice_bits, sifted_bob_bits):
    check_bits = random.choice(len(sifted_alice_bits), size=len(sifted_alice_bits) // 2, replace=False)
    errors = sum(sifted_alice_bits[check_bits] != sifted_bob_bits[check_bits])
    error_rate = errors / len(check_bits)
    return error_rate


main()

# Error correction?
# Simulation?
# Inter Device Connection? With 
# Messaging and Payment?
