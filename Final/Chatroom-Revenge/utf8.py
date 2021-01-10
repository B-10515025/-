str = [0,0,0]
total = 0
for i in range(237,239):
    for j in range(256):    
        ok = 0
        for k in range(256):
            str[0] = i
            str[1] = j
            str[2] = k
            try:
                bytes(str).decode('utf-8')
                ok += 1
            except UnicodeDecodeError:
                pass
        print(i,j,ok)
