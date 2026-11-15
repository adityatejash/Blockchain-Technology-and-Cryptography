from web3 import Web3
from eth_account import Account

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
eth = lambda wei: w3.from_wei(wei, "ether")
print("Network : Localhost 8545 | Chain ID:", w3.eth.chain_id, "| Currency: ETH")

# Step 1: Create a new wallet (like "Create a wallet" in MetaMask)
wallet = Account.create()
print("\n[1] New wallet created")
print("    Address :", wallet.address)
print("    Balance :", eth(w3.eth.get_balance(wallet.address)), "ETH")

# Step 2: Import a funded Ganache account (like "Import account" in MetaMask)
funded = Account.from_key(
    "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d")
print("\n[2] Account imported (Ganache account #0)")
print("    Address :", funded.address)
print("    Balance :", eth(w3.eth.get_balance(funded.address)), "ETH")


def send_eth(account, to, amount_eth):
    """Sign a transaction with the account's private key and broadcast it."""
    tx = {
        "nonce": w3.eth.get_transaction_count(account.address),
        "to": to,
        "value": w3.to_wei(amount_eth, "ether"),
        "gas": 21000,
        "gasPrice": w3.eth.gas_price,
        "chainId": w3.eth.chain_id,
    }
    signed = account.sign_transaction(tx)
    return w3.eth.send_raw_transaction(signed.raw_transaction)


# Step 3: Send 5 ETH to the new wallet
h1 = send_eth(funded, wallet.address, 5)
r1 = w3.eth.wait_for_transaction_receipt(h1)
print("\n[3] Sent 5 ETH : Account #0 -> New wallet")
print("    Tx hash :", h1.to_0x_hex())
print("    Block   :", r1.blockNumber, "| Gas used:", r1.gasUsed, "| Status: Confirmed")

# Step 4: Send 1.5 ETH from the new wallet to another account
receiver = w3.eth.accounts[1]
h2 = send_eth(wallet, receiver, 1.5)
print("\n[4] Sending 1.5 ETH : New wallet ->", receiver)
print("    Tx hash :", h2.to_0x_hex(), "(pending)")
r2 = w3.eth.wait_for_transaction_receipt(h2)
print("    Block   :", r2.blockNumber, "| Gas used:", r2.gasUsed, "| Status: Confirmed")
print("    Gas fee :", eth(r2.gasUsed * r2.effectiveGasPrice), "ETH")

# Step 5: Final balances
print("\n[5] Final balances")
print("    New wallet :", eth(w3.eth.get_balance(wallet.address)), "ETH")
print("    Receiver   :", eth(w3.eth.get_balance(receiver)), "ETH")

# Step 6: Transaction details
t = w3.eth.get_transaction(h2)
print("\n[6] Transaction details")
print("    From   :", t["from"])
print("    To     :", t["to"])
print("    Value  :", eth(t["value"]), "ETH")
print("    Nonce  :", t["nonce"])
print("    Block  :", t["blockNumber"])
