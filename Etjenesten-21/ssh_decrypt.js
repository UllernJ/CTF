//ingen fin kode, men det funker..:)
var sodium = require('sodium-native')

var nonce = Buffer.alloc(sodium.crypto_secretbox_NONCEBYTES)
var key = sodium.sodium_malloc(0x20) // secure buffer
var message = Buffer.from('username=user:timestamp=1641051525')
var ciphertext = Buffer.alloc(message.length + 0x10)

//6047ed1d2246dd7223946e61a3b3ade031e7bfd44e3fb02cd9ea492484f711bb

key[0] = 0x60
key[1] = 0x47
key[2] = 0xed
key[3] = 0x1d
key[4] = 0x22
key[5] = 0x46
key[6] = 0xdd
key[7] = 0x72
key[8] = 0x23
key[9] = 0x94
key[10] = 0x6e
key[11] = 0x61
key[12] = 0xa3
key[13] = 0xb3
key[14] = 0xad
key[15] = 0xe0
key[16] = 0x31
key[17] = 0xe7
key[18] = 0xbf
key[19] = 0xd4
key[20] = 0x4e
key[21] = 0x3f
key[22] = 0xb0
key[23] = 0x2c
key[24] = 0xd9
key[25] = 0xea
key[26] = 0x49
key[27] = 0x24
key[28] = 0x84
key[29] = 0xf7
key[30] = 0x11
key[31] = 0xbb
nonce[0] = 0;
// encrypted message is stored in ciphertext
sodium.crypto_secretbox_easy(ciphertext, message, nonce, key)

console.log('Encrypted message:', ciphertext)