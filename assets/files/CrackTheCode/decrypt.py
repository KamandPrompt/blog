from Crypto.Util.number import *
from Crypto.PublicKey import RSA
import gmpy2

def nth_root(x,n):
    """Finds the integer component of the n'th root of x,
    an integer such that y ** n <= x < (y + 1) ** n.
    """
    high = 1
    while high ** n < x:
        high *= 2
    low = high/2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1

f = open("publickeyz.pem",'r')
publickey = RSA.importKey(f.read())

cipherfile = open("ciphertextz.txt", 'r')
cipher = cipherfile.read()
cipher = bytes_to_long(cipher)
print long_to_bytes(nth_root(cipher,3),3)
