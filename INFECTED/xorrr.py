from pwn import xor
#We convert the cipher_text to bytes.
cipher_text = bytes.fromhex("49b4469b43ae459a7ba230ac5f9353816da35fb8348c30ab729337bb5fb9528750cd30a3")
#We declare that we know the first 4 letters in the cipher text and that way we can get the key or the partial key.
partial_key = xor(cipher_text[:4], 'INFE')
#In this case we get the whole key and can decrypt the whole cipher text.
print(xor(cipher_text, partial_key).decode('utf-8'))