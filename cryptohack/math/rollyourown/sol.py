from Crypto.Util.number import bytes_to_long, long_to_bytes
import telnetlib
import json
from sage.all import *
    
HOST = "socket.cryptohack.org"
PORT = 13403

def check_params(data, q):
    g = int(data['g'], 16)
    n = int(data['n'], 16)
    if g < 2:
        return False
    elif n < 2:
        return False
    elif pow(g,q,n) != 1:
        return False
    return True

def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline().decode()
    st = line[line.find('{'):]
    return json.loads(st)

def json_send(hsh):
    request = json.dumps(hsh).encode()
    tn.write(request)
    
tn = telnetlib.Telnet(HOST, PORT)

get_str = readline().decode()
 
q = int(get_str[18:-2],0)
g = q+1
n = q*q

stri = '''{"g" : "{g}", "n" : "{n}"}'''
to_send = json.loads(stri)
to_send["g"] = hex(g)
to_send["n"] = hex(n)

json_send(to_send)

get_str = readline().decode()

g_x = int(get_str[72:-2],0)
x = (g_x-1)//q

stri = '''{"x" : "{x}"}'''
to_send = json.loads(stri)
to_send["x"] = hex(x)

json_send(to_send)

get_str = readline().decode()
print(get_str)
