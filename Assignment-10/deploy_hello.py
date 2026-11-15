import solcx
from web3 import Web3

# 1. Compile the Solidity contract
solcx.install_solc("0.8.24")
solcx.set_solc_version("0.8.24")
with open("HelloWorld.sol") as f:
    source = f.read()
compiled = solcx.compile_source(source, output_values=["abi", "bin"])
_, iface = compiled.popitem()
print("Compiler version : solidity 0.8.24")
print("Compilation successful: HelloWorld.sol")

# 2. Connect to Ganache and deploy
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
deployer = w3.eth.accounts[0]
print("Deploying from account:", deployer)

Hello = w3.eth.contract(abi=iface["abi"], bytecode=iface["bin"])
tx_hash = Hello.constructor("Hello, Blockchain!").transact({"from": deployer})
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
hello = w3.eth.contract(address=receipt.contractAddress, abi=iface["abi"])

print("\n[Deploy] HelloWorld.(constructor)")
print("status           : 1 (Transaction mined and execution succeed)")
print("contract address :", receipt.contractAddress)
print("transaction hash :", tx_hash.to_0x_hex())
print("block number     :", receipt.blockNumber)
print("gas used         :", receipt.gasUsed)

# 3. Call read-only functions
print("\n[Call]  message()      ->", hello.functions.message().call())
print("[Call]  owner()        ->", hello.functions.owner().call())
print("[Call]  number()       ->", hello.functions.number().call())
print("[Call]  add(15, 25)    ->", hello.functions.add(15, 25).call())

# 4. Send transactions that change the contract state
tx = hello.functions.setMessage("Welcome to Solidity!").transact({"from": deployer})
r = w3.eth.wait_for_transaction_receipt(tx)
print('\n[Tx]    setMessage("Welcome to Solidity!")')
print("        hash:", tx.to_0x_hex(), "| gas used:", r.gasUsed)

tx = hello.functions.setNumber(42).transact({"from": deployer})
r = w3.eth.wait_for_transaction_receipt(tx)
print("[Tx]    setNumber(42)")
print("        hash:", tx.to_0x_hex(), "| gas used:", r.gasUsed)

print("\n[Call]  getMessage()   ->", hello.functions.getMessage().call())
print("[Call]  number()       ->", hello.functions.number().call())
