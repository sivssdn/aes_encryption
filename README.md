# Key Generation steps
 - Choose a 300-bit prime p.
 - Choose a generator g of the cyclic group Zp*
 - Choose a number a uniformly at random from the set {2, 3, . . . , p - 2}.
 - Compute h = g^a mod p (using square and multiply)
 - PublicKey = (p, g, h)
 - SecretKey = a

# Encryption: 
The input to this algorithm is a message-file F and the PublicKey (p, g, h). It outputs a encryption of F as follows:
 - Choose a random key K from the set {0,1}^128
 - Compute C1 = AES.Enc(F, K) [using pycrypto]
 - Compute K' = int(K), where int(K) denotes the integer value of K.
 - Choose a number r uniformly at random from the set {0, 1, . . . , p - 2}
 - Compute C2 = g^r mod p, and C3 = K'h^r mod p (square and multiply)
 - Output a ciphertext C = C1, C2, C3

# Decryption: 
The input to this algorithm is a ciphertext C = C1, C2, C3 and the SecretKey a. It returns a plaintext and file as follows:
 - Compute C2' = C2^a mod p (square and multiply)
 - Compute K' = C3(C2')^-1 mod p (Euclidean algo. for inverse)
 - Compute K = Bin(K'), where Bin(K') turns K' into binary
 - Compute F = AES.Dec(C1, K) [using pycrypto]
 - output F