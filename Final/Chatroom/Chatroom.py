from pwn import *

#flag =       }\x00\x00
#0x307234 0x455665 0x7d0000

#target = 1110 0111 1001 0100 1011 0111
#bit = [0011 01 00 0100 01 01 0111 00 00]
bit = [[7,0,0],[4,4,4],[3,4,0]]

char = [48,49,50,51,52,53,54,55,56,57,97,98,99,100,101,102]

def setValue(data,position,value,length):
    arr = bytearray(data)
    for i in range(length):
        arr[position] = char[int(value % 16)]
        value = int(value / 16)
        position -= 1
    return bytes(arr)

print('男'.encode('utf-8'))
#server = process(['python3','server.py'])
server = remote('eofqual.zoolab.org',10110)
server.recvuntil('聊天室房間號碼: ')
cipher = server.recvline()[:-33]
print(cipher.decode())

part = 0
while len(cipher) > 16:
    print(cipher[-32:-16].decode(),cipher[-16:].decode())
    oi = cipher[-32:-16]
    for i in range(65536):
        if i % 1024 == 0:
            print(i)
        iv = cipher[-32:-16]
        prebit = [14,9,11]
        for k in range(3):
            prebit[k] = prebit[k]^bit[part][k]^char.index(iv[10+k*2])
            if k > 0:
                prebit[k] = prebit[k] & 12
        iv = setValue(iv,11,prebit[0] * 16 + int(i / 4096),2)
        iv = setValue(iv,13,prebit[1] * 16 + int((i % 4096) / 64), 2)
        iv = setValue(iv,15,prebit[2] * 16 + int(i % 64), 2)
        server.recvuntil('輸入訊息: ')
        server.sendline(iv + cipher[-16:])
        response = server.recvline()[:-1]
        if response.decode() == '系統訊息: 對方離開了，請按離開按鈕回到首頁':
            print(iv)
            break
    target = [14,7,9,4,11,7]
    str = [0,0,0]
    for t in range(3):
        str[t] = (target[t*2]^char.index(iv[10+t*2])^char.index(oi[10+t*2])) * 16 + (target[t*2+1]^char.index(iv[10+t*2+1])^char.index(oi[10+t*2+1]))
    print(bytes(str))
    aiv = cipher[-32:-16]
    aiv = iv
    position = 9
    while position > 0:
        niv = cipher[-32:-16]
        for i in range(4):
            niv = setValue(niv,position+1+i,char.index(aiv[position+1+i])^target[i]^target[i+2],1)
        find = False
        for i in range(256):
            niv = setValue(niv,position,i,2)
            server.recvuntil('輸入訊息: ')
            server.sendline(niv + cipher[-16:])
            response = server.recvline()[:-1]
            if response.decode() == '系統訊息: 對方離開了，請按離開按鈕回到首頁':
                print(niv)
                aiv = niv
                find = True
                break
        if find:
            for t in range(3):
                str[t] = (target[t*2]^char.index(niv[position-1+t*2])^char.index(oi[position-1+t*2])) * 16 + (target[t*2+1]^char.index(niv[position-1+t*2+1])^char.index(oi[position-1+t*2+1]))
            print(bytes(str))
        position -= 2
    cipher = cipher[:-16]
    part += 1

