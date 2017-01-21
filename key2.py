from miller import *
import math
def modexp( base, exp, modulus ):
        return pow(base, exp, modulus)
def loopIsPrime(number):
	#looping to reduce probability of rabin miller false +
	isNumberPrime = True
	for i in range(0,20):
		isNumberPrime*=isPrime(number)
		if(isNumberPrime == False):
			return isNumberPrime
	return isNumberPrime	
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
def keyGeneration():
	x=False;
		
	while(x == False):
		#p1=generateLargePrime(150)
		p1=generateLargePrime(150)
		p2=generateLargePrime(150)
		print(len(str(p1)))
		p=(p1*p2*2)+1
		
		#x = isPrime(p)
		x=loopIsPrime(p)
		
		if(x == True):
			y = False
			#print("p1 - ",p1,"\n")
			#print("p2 - ",p2,"\n")
			#print("p - ",p,"\n")
			while(y == False):
				
				g=random.randint(2, p-1)
				#if(((g**(p1*p2)-1)%p != 0) and ((g**(p1*2)-1)%p != 0) and ((g**(2*p2)-1)%p != 0)):
				if not (modexp(g, (p-1)//2,p) == 1):
					if not (modexp(g, (p-1)//p1, p) == 1):
						
						y=True
						#we have g now
						a = random.randint(2, p-2)
						#h as per question var names
						hh = squareAndMultiply(g,a,p)
						print("p = ", p)
						print("g = ",g)
						print("h = ",hh)
						print("a = ",a)
						#write to file key.txt
					
keyGeneration()