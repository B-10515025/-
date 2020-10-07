import random as rand
from typing import List as list


def convert(data, size=4):
    return [int.from_bytes(data[index:index+size], 'big') for index in range(0, len(data), size)]

def Inverse(data, size=4):
    s = b''.join([d.to_bytes(size, 'big') for d in data])
    return b''.join([d.to_bytes(size, 'big') for d in data])

def _Decrypt(vector: list[int], key: list[int]):
    sum, delta, mask = 0x59D60180, 0xFACEB00C, 0xffffffff
    for 次數 in range(32):
        vector[1] = vector[1] - ((vector[0] << 4) + key[2] & mask ^ (vector[0] + sum) & mask ^ (vector[0] >> 5) + key[3] & mask) & mask
        vector[0] = vector[0] - ((vector[1] << 4) + key[0] & mask ^ (vector[1] + sum) & mask ^ (vector[1] >> 5) + key[1] & mask) & mask
        sum = sum - delta & mask
    return vector

def Decrypt(cipher: bytes, key: bytes):
    plain = b''
    for index in range(0, len(cipher), 8):
        plain += Inverse(_Decrypt(convert(cipher[index:index+8]), convert(key)))
    return plain

if __name__ == '__main__':
    code = b'w\xf9\x05\xc3\x9e6\xb5\xeb\r\xee\xcb\xb4\xeb\x08\xe8\xcb'
    seed = 1600000000
    while seed > 0:
        rand.seed(seed)
        key = rand.getrandbits(128).to_bytes(16, 'big')
        flag = Decrypt(code, key)
        if flag[:4] == b'FLAG':
            print(flag.decode())
            break
        seed -= 1
