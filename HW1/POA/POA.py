from pwn import *

char = [48,49,50,51,52,53,54,55,56,57,97,98,99,100,101,102]

def setValue(data,position,value):
    arr = bytearray(data)
    arr[position] = char[int(value / 16)]
    arr[position + 1] = char[int(value % 16)]
    return bytes(arr)

def accept(input):
    server.recvuntil('cipher = ')
    server.sendline(input)
    response = server.recvline()
    return response == b'YESSSSSSSS\n'

def getXor(decode,cipher):
    arr = bytearray(decode)
    i = len(cipher) - 33
    while i >= len(cipher) - 64:
        arr[i] = char[char.index(decode[i]) ^ char.index(cipher[i])]
        i -= 1
    return bytes(arr)

def getPlain(cipher):
    input = cipher
    position = len(cipher) - 34
    while position >= len(cipher) - 64:
        v = 0
        while v < 256:
            input = setValue(input,position,v)
            if accept(input):
                break
            v += 1
        if position == 0 or (accept(setValue(input,position - 2,0)) and accept(setValue(input,position - 2,1))):
            if v < 128:
                input = setValue(input,position,v + 128)
            else:
                input = setValue(input,position,v - 128)
        position -= 2
    return getXor(input,cipher)[-64:-32]

#server = process(['python3','server.py'])
server = remote('140.112.31.97',30000)
server.recvuntil('cipher = ')
cipher = server.recvline()[:-1]
flag = b''
while len(cipher) > 32:
    flag = getPlain(cipher) + flag
    cipher = cipher[:-32]
while flag[-2:] == b'00':
    flag = flag[:-2]
if flag[-2:] == b'80':
    flag = flag[:-2]
    print(bytearray.fromhex(flag.decode()).decode())
else:
    print("something error.")
