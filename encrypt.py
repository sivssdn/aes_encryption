import random
import base64
from Crypto.Cipher import AES
from Crypto import Random
import os, random, struct,sys
from Crypto.Cipher import AES

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        #out_filename = in_filename + '.enc'
	out_filename = 'cipherFile.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
 
def binaryRandom():
	#generating 128 bit random number
	k=""
	for i in range(0,128):
		k = k+str(random.randint(0,1))
	#print(len(str(k)))
	return k
def _chunks(string, chunk_size):
	for i in range(0, len(string), chunk_size):
		yield string[i:i+chunk_size]
def encryption():

	try:
		inputFile = sys.argv[1]
	except IndexError:
		print("Please pass the filename to be encrypted as first program argument")
		sys.exit()
	k = binaryRandom()
	print("Encrypting...")
	#converting 128 bits to 16bytes hexadecimal representation
	stringHex = ''.join('{:02x}'.format(int(b,2)) for b in _chunks(k,8))
	#print(stringHex)
	strinHextoInt = '0x'+stringHex
	#print(int(strinHextoInt,16))
	k=int(strinHextoInt,16) #converting k to int
	#print(hex(k))

	
	#get p, g, h from file
	file1 = open("key.txt",'r')
	p = long(file1.readline())
	g = long(file1.readline())
	h = long(file1.readline())

	r=random.randint(0, p)
	cipher2 = squareAndMultiply(g,r,p)
	#k = long(k)
	cipher3 = (k*squareAndMultiply(h,r,p))%p
	
#	filec2 = open("cipher2.txt","w")
#	filec3 = open("cipher3.txt","w")
#	filec2.write(str(cipher2))
#	filec3.write(str(cipher3))
	
	#encrypt the file

	encrypt_file(stringHex,inputFile)
	#we have the encrypted file, now in new file write cipher2 and cipher3 along with all the contents of .enc file
	cipherFile = open("cipherFile.enc","rb")
	newCipherFile = open("cipherFile","wb")
	newCipherFile.write(str(cipher2))
	newCipherFile.write("\n")
	newCipherFile.write(str(cipher3))
	newCipherFile.write("\n")
	newCipherFile.write(str(inputFile))
	newCipherFile.write("\n")
	for line in cipherFile:
		newCipherFile.write(line)
	cipherFile.close()
	newCipherFile.close()
	file1.close()
	os.remove("cipherFile.enc")
	print_message ="Encrypted file stored under name : cipherFile"
	print(print_message)
def squareAndMultiply(x,c,n):
	z=1
	#getting value of l by converting c into binary representation and getting its length
	c="{0:b}".format(c)[::-1] #reversing the binary string
	
	l=len(c)
	for i in range(l-1,-1,-1):
		z=pow(z,2)
		z=z%n
		if(c[i] == '1'):
			z=(z*x)%n
	return z	

encryption()

