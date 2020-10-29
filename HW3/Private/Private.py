from web3 import Web3,HTTPProvider

w3 = Web3(HTTPProvider(r"https://ropsten.infura.io/v3/6a17ad8ec1ff4b5c97d809725b515aac"))
contractAddress = open('./ContractAddress').read()
flag = w3.eth.getStorageAt(contractAddress, 0)[0:-1].decode()
print(flag)