from pwn import *

context.arch = 'amd64'
shellcode = asm('''
                push   r13
                push   r12
                ''')
print(shellcode.hex())
