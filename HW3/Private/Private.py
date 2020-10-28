from web3 import Web3,HTTPProvider

w3 = Web3(HTTPProvider(r"https://ropsten.infura.io/v3/6a17ad8ec1ff4b5c97d809725b515aac"))
flag = w3.eth.getStorageAt('0x21546F53AC81DDfc2b618D5617d173e43661366c', 0).decode()
print(flag)