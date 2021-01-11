T = 0xe794b7
I = 0x33e5e2

I4 = [0x21ff41,0xb3423c,0x7d611b]
P4 = [0xf619c2,0x1180ee,0xe7f5ac]
F4 = [0,0,0]
for i in range(3):
    F4[i] = I4[i]^P4[i]^T
    print(hex(F4[i]))
b = [48,49,50]
print(bytes(b).decode())

