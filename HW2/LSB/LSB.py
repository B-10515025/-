from pwn import *

def findRange(L, H, E, N, T):
    M = (L + H) // 2
    m0 = ((L * E) % N) % 3
    m1 = ((M * E) % N) % 3
    m2 = ((H * E) % N) % 3
    pL = L
    pH = M
    p1 = (pL + pH) // 2
    while ((p1 * E) % N) % 3 == (((p1 + 1) * E) % N) % 3:
        if ((p1 * E) % N) % 3 == m0:
            pL = p1
        else:
            pH = p1
        p1 = (pL + pH) // 2
    pL = M
    pH = H
    p2 = (pL + pH) // 2
    while ((p2 * E) % N) % 3 == (((p2 + 1) * E) % N) % 3:
        if ((p2 * E) % N) % 3 == m1:
            pL = p2
        else:
            pH = p2
        p2 = (pL + pH) // 2
    if T == m0:
        return L, p1
    elif T == m1:
        return p1 + 1, p2
    else:
        return p2 + 1, H

#server = process(['python3','server.py'])
server = remote('140.112.31.97',30001)

server.recvuntil('n = ')
n = int(server.recvline())
server.recvuntil('c = ')
c = int(server.recvline())
e = 65537

L = 0
H = n - 1
E = 1
t = pow(3, e, n)
while H != L:
    c = (t * c) % n
    E *= 3
    server.sendline(str(c))
    server.recvuntil('m % 3 =')
    k = int(server.recvline())
    L, H = findRange(L, H, E, n, k)
flag = L.to_bytes(128, byteorder="big")
pos = 0
for i in range(len(flag)):
    if flag[i] == 0:
        pos = i + 1
flag = flag[pos:].decode()
print(flag)