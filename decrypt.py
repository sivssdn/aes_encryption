import random
import base64
import math
from Crypto.Cipher import AES
from Crypto import Random
import os, random, struct

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
def decryption():
	print("Decrypting from file named 'cipherFile' ")
	fileobj = open("cipherFile","r")
	cipher2 = long(fileobj.readline())
	cipher3 = long(fileobj.readline())
	outputFilename = 'decrypted_'+fileobj.readline().rstrip()

	#filec2 = open("cipher2.txt","r")
	#filec3 = open("cipher3.txt","r")
	secretfile = open("secretkey.txt","r")
	#cipher2 = long(filec2.readline())
	#cipher3 = long(filec3.readline())
	p = long(secretfile.readline())
	a = long(secretfile.readline())
	
	cipher2dash = squareAndMultiply(cipher2,a,p)
	kdash = (cipher3*squareAndMultiply(cipher2dash,p-2,p))%p

	k=str(hex(kdash))
	k=k[2:-1] #striping character from hex string
	#print(k)

#now we have the key, copy the encrypted file to temp file without cipher2 and cipher3 and then decrypt
	tmp = open("temp.enc","wb")
	for line in fileobj:
		tmp.write(line)
	tmp.close()
	decrypt_file(k, "temp.enc",outputFilename)
	os.remove("temp.enc")
	print(" \n Decrypted file stored as : ",outputFilename)

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
	
#function to compute inverse
def computeInverse (in1,in2):
    aL = [in1]
    bL = [in2]
    tL = [0]
    t = 1
    sL = [1]
    s = 0
    q = math.floor((aL[0]/bL[0]))
    r = (aL[0] - (q*bL[0]))

    while r > 0 :
        temp = (tL[0] - (q*bL[0]))
        tL[0] = t
        t = temp
        temp = (sL[0] - (q*s))
        sL[0] = s
        s = temp
        aL[0] = bL[0]
        bL[0] = r
        q = math.floor(aL[0]/bL[0])
        r = (aL[0] - (q*bL[0]))

    r = bL[0]

    inverse = s % in2
    return inverse

decryption()
