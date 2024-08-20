import json
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from hashlib import sha256
from base64 import b64decode
import math

with open('bobs-key.json', "r") as b_sk:
    x = json.loads(b_sk.readline())
    N = x['N']
    Db = x['D']

with open('carols-key.json', "r") as c_sk:
    x = json.loads(c_sk.readline())
    Dc = x['D']

with open('message.json', "r") as m:
    x = json.loads(m.readline())
    V = x['V']
    Nonce = b64decode(x['Nonce'])
    Body = b64decode(x['Body'])

# go run util.go common.go
Na = 68466124358447043964793860695303219539650445665911634985762693469730327004150221093834311733904797348442799908399246730582062642263634283446861336873461968502263337629342332438783884701131347313176600603933876770574183288847451569562402716371409261964555755051621978414707323660060294173332302171179832532379
Nb = 110986239228452276705243281071881479737523902719947647938060491211704764431880660457345141212455880526555282371426548091232174507173827515718646915260209209310984096008076553763193605528007494132681243769355257049176601319896119207555664923628139878933762458235186384695655511029359951266896240850577326410847
Nc = 18582276766855359825862402926962157340924980281247327659493110701005516273379320985882651365698262102353632527841385001594558813158406233076564558107185915033432517721563838890277476493080671924187822252392601964872884236885867485941435462493387367059855066030863330998063048539162355605905139712812660046019

A = 1 + (Na-Nb)*Db
B = 1 + (Na-Nc)*Dc

print(A, B)

def xgcd_nonrecursive(a, b):
	""" Calculates the gcd and Bezout coefficients, 
	using the Extended Euclidean Algorithm (non-recursive).
	(Source: extendedeuclideanalgorithm.com/code) 
	"""
	#Set default values for the quotient, remainder, 
	#s-variables and t-variables
	q = 0
	r = 1
	s1 = 1 
	s2 = 0
	s3 = 1 
	t1 = 0 
	t2 = 1
	t3 = 0
	
	'''
	In each iteration of the loop below, we
	calculate the new quotient, remainder, a, b,
	and the new s-variables and t-variables.
	r decreases, so we stop when r = 0
	'''
	while(r > 0):
		#The calculations
		q = math.floor(a/b)
		r = a - q * b
		s3 = s1 - q * s2
		t3 = t1 - q * t2
		
		'''
		The values for the next iteration, 
		(but only if there is a next iteration)
		'''
		if(r > 0):
			a = b
			b = r
			s1 = s2
			s2 = s3
			t1 = t2
			t2 = t3

	return abs(b), s2, t2 

_, X, Y = xgcd_nonrecursive(A,B)
X = int(X)
Y = int(Y)

d = X*Db + Y*Dc 
K = pow(V,d,N)
print(K)

print(Nonce)

shared = sha256(long_to_bytes(K)).digest()
aes = AES.new(shared, AES.MODE_GCM, nonce=Nonce)
print(aes.decrypt(Body))
