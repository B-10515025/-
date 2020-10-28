from web3 import Web3, HTTPProvider
from solc import compile_files
import os

myAddress = '0xB3580FB6944BC704149CE71DF2247897755Ba7d7'
myKey = '0x7613f3f0e75e124b78280cde672d5870ea87ebdea19aca556e1c6a720e8fbe82'
w3 = Web3(HTTPProvider(r'https://ropsten.infura.io/v3/6a17ad8ec1ff4b5c97d809725b515aac'))

def call(function):
    txn = function.buildTransaction({'nonce': w3.eth.getTransactionCount(myAddress), 'gas': w3.eth.getBlock("latest").gasLimit, 'gasPrice': w3.toWei('1000', 'gwei')})
    sign = w3.eth.account.sign_transaction(txn, myKey)
    w3.eth.sendRawTransaction(sign.rawTransaction)

os.environ['SOLC_BINARY'] = '/mnt/c/Users/B10515025/Desktop/NTUST_CTF/HW3/solc.exe'
ALL_OUTPUT_VALUES = ("abi", "asm", "ast", "bin", "bin-runtime", "devdoc", "interface", "opcodes", "userdoc",)
compiled_sol = compile_files(['./GetStarted.sol'], output_values = ALL_OUTPUT_VALUES) 

GetStartedFactory = w3.eth.contract(address = '0x16cf9e5a5848E40E27751f1c9277291993fE6C4E', abi = compiled_sol['./GetStarted.sol:GetStartedFactory']['abi'])
instance = GetStartedFactory.functions.instances(myAddress).call()

if instance == '0x0000000000000000000000000000000000000000':
    call(GetStartedFactory.functions.create())
    print("Instance created.")
else:
    GetStarted = w3.eth.contract(address = instance, abi = compiled_sol['./GetStarted.sol:GetStarted']['abi'])
    win = GetStarted.functions.win().call()
    print(win)
    if win:
        print("Enter token:")
        token = input()
        call(GetStartedFactory.functions.validate(int(token, 16)))
    else:
        call(GetStarted.functions.callme())
        print("Called to win.")