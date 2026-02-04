from pwn import *

p = process("./solveMe.o")
#1
p.recvuntil(b":")
p.sendline(b"SuperSecretPass!")
#2
p.recvuntil(b":")
p.sendline(b"a beautiful pass")
#3

expected = [-0x708baa70, 0x6b838889, 0x8c5d8485, 0x6283616a]
password = []
local_e8 = 0

for i in range(4):
    local_dc = local_e8 * 0x1010101 + 0x10203
    local_e8 += 4
    
    chunk = ((expected[i] - 0x23232323) ^ local_dc)
    for j in range(4):
        password.append(chr((chunk >> (j * 8)) & 0xFF))
password = ''.join(password)
print(password)
p.recvuntil(b":")
p.sendline(password.encode())

#4 found in solveMeBrute
p.recvuntil(b":")
p.sendline(b"qbit")
p.interactive()
# Generate all combinations
