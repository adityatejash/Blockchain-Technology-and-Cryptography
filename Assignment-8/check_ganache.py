from web3 import Web3

# Connect to the local Ganache node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    raise SystemExit("Could not connect to Ganache on port 8545")

print("Connected to local Ethereum node at http://127.0.0.1:8545")
print("Chain ID     :", w3.eth.chain_id)
print("Client       :", w3.client_version)
print("Block number :", w3.eth.block_number)

print("\nAvailable accounts:")
for acc in w3.eth.accounts:
    balance = w3.from_wei(w3.eth.get_balance(acc), "ether")
    print(f"  {acc}  {balance} ETH")

# Send a test transaction: 1 ETH from account[0] to account[1]
sender, receiver = w3.eth.accounts[0], w3.eth.accounts[1]
tx_hash = w3.eth.send_transaction({
    "from": sender,
    "to": receiver,
    "value": w3.to_wei(1, "ether"),
})
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("\nTest transaction: 1 ETH from account[0] to account[1]")
print("  Tx hash    :", receipt.transactionHash.to_0x_hex())
print("  Block      :", receipt.blockNumber)
print("  Gas used   :", receipt.gasUsed)
print("  Status     :", "Success" if receipt.status == 1 else "Failed")

print("\nBalance account[0]:", w3.from_wei(w3.eth.get_balance(sender), "ether"), "ETH")
print("Balance account[1]:", w3.from_wei(w3.eth.get_balance(receiver), "ether"), "ETH")
print("Block number now  :", w3.eth.block_number)
