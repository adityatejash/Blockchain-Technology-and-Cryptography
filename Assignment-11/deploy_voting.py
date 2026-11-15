import re

import solcx
from eth_abi import decode
from web3 import Web3
from web3.logs import DISCARD


def revert_reason(e):
    """Decode the Error(string) revert message from the exception data."""
    m = re.search(r"0x08c379a0([0-9a-fA-F]+)", str(e))
    if m:
        return decode(["string"], bytes.fromhex(m.group(1)))[0]
    return str(e)


solcx.install_solc("0.8.24")
solcx.set_solc_version("0.8.24")
with open("Voting.sol") as f:
    compiled = solcx.compile_source(f.read(), output_values=["abi", "bin"])
iface = compiled["<stdin>:Voting"]
print("Compilation successful: Voting.sol (Ownable, Voting)")

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
owner, v1, v2, v3, v4 = w3.eth.accounts[:5]

Voting = w3.eth.contract(abi=iface["abi"], bytecode=iface["bin"])
tx = Voting.constructor().transact({"from": owner})
rc = w3.eth.wait_for_transaction_receipt(tx)
voting = w3.eth.contract(address=rc.contractAddress, abi=iface["abi"])
print("Voting deployed at :", rc.contractAddress)
print("Owner              :", voting.functions.owner().call())
print("Deploy gas used    :", rc.gasUsed)

STATES = ["Created", "Voting", "Ended"]


def short(v):
    return v[:10] + ".." if isinstance(v, str) and v.startswith("0x") else v


def send(label, fn, sender):
    """Run a contract function; print events on success, reason on revert."""
    try:
        fn.call({"from": sender})            # dry-run to catch revert reasons
    except Exception as e:
        reason = revert_reason(e)
        print(f'[REVERT] {label} -> "{reason}"')
        return
    receipt = w3.eth.wait_for_transaction_receipt(fn.transact({"from": sender}))
    print(f"[OK]     {label} | gas {receipt.gasUsed}")
    for ev in (voting.events.CandidateAdded, voting.events.Voted,
               voting.events.StateChanged):
        for log in ev().process_receipt(receipt, errors=DISCARD):
            args = ", ".join(str(short(v)) for v in log.args.values())
            print(f"         event {log.event}({args})")


print("\n-- Adding candidates --")
send('addCandidate("Alice")', voting.functions.addCandidate("Alice"), owner)
send('addCandidate("Bob")', voting.functions.addCandidate("Bob"), owner)
send('addCandidate("Carol")', voting.functions.addCandidate("Carol"), owner)

print("\n-- Access control test --")
send('addCandidate("Mallory") by non-owner', voting.functions.addCandidate("Mallory"), v1)
send("vote(1) before voting starts", voting.functions.vote(1), v1)

print("\n-- Start voting --")
send("startVoting()", voting.functions.startVoting(), owner)

print("\n-- Casting votes --")
send("vote(1) by voter1", voting.functions.vote(1), v1)
send("vote(2) by voter2", voting.functions.vote(2), v2)
send("vote(1) by voter3", voting.functions.vote(1), v3)
send("vote(2) by voter1 (double vote)", voting.functions.vote(2), v1)
send("vote(9) by voter4 (invalid id)", voting.functions.vote(9), v4)

print("\n-- Results --")
send("endVoting()", voting.functions.endVoting(), owner)
for i in range(1, voting.functions.candidatesCount().call() + 1):
    cid, name, votes = voting.functions.candidates(i).call()
    print(f"Candidate {cid}: {name:<6} votes = {votes}")

winner, votes = voting.functions.getWinner().call()
print(f"\nWinner: {winner} with {votes} votes")
print("Final state:", STATES[voting.functions.state().call()])
