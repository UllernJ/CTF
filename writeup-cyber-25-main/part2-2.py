import hashlib

def sha256(val: str) -> bytes:
    return hashlib.sha256(val.encode()).digest()

def xor(a: bytes, b: bytes) -> bytearray:
    out = bytearray(a)
    for i in range(len(out)):
        out[i] = a[i] ^ b[i]
    return out
        
def getUserSignature(username: str):
    userHash = sha256(username)
    seedHash = sha256("")
    signature = xor(userHash, seedHash)
    return signature.hex()

print(getUserSignature("Chris Adams"))