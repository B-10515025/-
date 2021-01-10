from pwn import *
from hashlib import md5

char = [48,49,50,51,52,53,54,55,56,57,97,98,99,100,101,102]

def c(hex):
    return char.index(hex)
    
def setValue(data,position,value,length):
    arr = bytearray(data)
    for i in range(length):
        arr[position] = char[int(value % 16)]
        value = int(value / 16)
        position -= 1
    return bytes(arr)

server = process(['python3','server.py'])
#server = remote('eofqual.zoolab.org',10111)
server.recvuntil('聊天室房間號碼: ')
code = server.recvline()[:-1]
cipher = code[:-32]
MD5hash = code[-32:].decode()
print(cipher.decode())
print(MD5hash)

hexflag = b''
while len(cipher) > 16:
    print(cipher[-32:-16].decode(),cipher[-16:].decode())
    part = cipher[-32:-16]
    ov = cipher[-32:-16]
    iv = cipher[-32:-16]
    dc = cipher[-32:-16]
    for f in range(256):
        v = 255 - f
        for i in range(8):
            part = setValue(part,i*2+1,int(v%2)*128,2)
            v = int(v/2)
        find = True
        for position in range(8):
            iv = cipher[-32:-16]
            for i in range(16):
                iv = setValue(iv,i,c(iv[i])^c(part[i]),1)
            ok = 0
            for i in range(4):
                iv = setValue(iv,position*2+1,i*64,2)
                server.recvuntil('輸入訊息: ')
                server.sendline(iv + cipher[-16:])
                response = server.recvline()[:-1]
                if response.decode() == '陌生人: 哈哈哈哈':
                    ok += 1
            if ok != 2:
                find = False
        if find:
            break
    print(part,'8/64')

    dc = cipher[-32:-16]
    for i in range(16):
        dc = setValue(dc,i,c(dc[i])^c(part[i]),1)
    for position in range(7):
        iv = dc
        last = 0
        for prev in range(16):
            iv = setValue(iv,position*2+1,prev*16,2)
            ok = 0
            for i in range(4):
                iv = setValue(iv,position*2+3,i*64,2)
                server.recvuntil('輸入訊息: ')
                server.sendline(iv + cipher[-16:])
                response = server.recvline()[:-1]
                if response.decode() == '陌生人: 哈哈哈哈':
                    ok += 1
                    last = i
            if ok == 1:
                part = setValue(part,position*2,(prev^c(ov[position*2])^12)&14,1)
                if position == 6:
                    part = setValue(part,position*2+2,((last*4)^c(ov[position*2+2])^8)&12,1)
                break
    print(part,'23/64')      

    dc = cipher[-32:-16]
    for i in range(16):
        dc = setValue(dc,i,c(dc[i])^c(part[i]),1)
    for position in range(7):
        iv = dc
        for prev in range(32):
            iv = setValue(iv,position*2+1,((c(dc[position*2])^12)&14)*16+prev,2)
            ok = 0
            for i in range(4):
                iv = setValue(iv,position*2+3,i*64,2)
                server.recvuntil('輸入訊息: ')
                server.sendline(iv + cipher[-16:])
                response = server.recvline()[:-1]
                if response.decode() == '陌生人: 哈哈哈哈':
                    ok += 1
            if ok == 0:
                part = setValue(part,position*2+1,c(part[position*2])*16+((prev^(c(ov[position*2])*16+c(ov[position*2+1])))&30),2)
                break
    print(part,'51/64')
    
    dc = cipher[-32:-16]
    for i in range(16):
        dc = setValue(dc,i,c(dc[i])^c(part[i]),1)
    for position in range(6):
        iv = dc
        iv = setValue(iv,position*2+1,(c(iv[position*2])*16+c(iv[position*2+1]))^224,2)
        iv = setValue(iv,position*2+3,(c(iv[position*2+2])*16+c(iv[position*2+3]))^128,2)
        iv = setValue(iv,position*2+5,(c(iv[position*2+4])*16+c(iv[position*2+5]))^128,2)
        server.recvuntil('輸入訊息: ')
        server.sendline(iv + cipher[-16:])
        response = server.recvline()[:-1]
        if response.decode() == '陌生人: 哈哈哈哈':
            part = setValue(part,position*2+1,c(part[position*2+1])^1,1)
    print(part,'57/64')
    
    hexflag = part + hexflag
    cipher = cipher[:-16]
    
i = 0
arr = []
while i < len(hexflag):
    arr.append(c(hexflag[i])*16+c(hexflag[i+1]))
    i += 2
while arr[-1] == 0:
    arr.pop()
flag = bytes(arr)
bits = 2**(7*int(len(flag)/8))

for i in range(bits):
    value = i
    arr = bytearray(flag)
    for block in range(int(len(flag)/8)):
        val = value % (2**7)
        a = int(val / (2**6))
        b = int(val % (2**6))
        arr[block*8+6] = (arr[block*8+6] & 254) + a
        arr[block*8+7] = (arr[block*8+7] & 192) + b
        value = value / (2**7)
    flag = bytes(arr)
    if md5(flag).hexdigest() == MD5hash:
        print(flag.decode())
        break