import re

import solcx
from eth_abi import decode
from web3 import Web3


def revert_reason(e):
    """Decode the Error(string) revert message from the exception data."""
    m = re.search(r"0x08c379a0([0-9a-fA-F]+)", str(e))
    if m:
        return decode(["string"], bytes.fromhex(m.group(1)))[0]
    return str(e)


solcx.install_solc("0.8.24")
solcx.set_solc_version("0.8.24")
with open("Crowdfunding.sol") as f:
    compiled = solcx.compile_source(f.read(), output_values=["abi", "bin"])
iface = compiled["<stdin>:Crowdfunding"]
print("Compilation successful: Crowdfunding.sol")

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
owner, donor_a, donor_b, donor_c = w3.eth.accounts[:4]
eth = lambda wei: f"{w3.from_wei(wei, 'ether')} ETH"


def deploy(title, goal_eth):
    Crowd = w3.eth.contract(abi=iface["abi"], bytecode=iface["bin"])
    tx = Crowd.constructor(title, w3.to_wei(goal_eth, "ether"), 3600).transact({"from": owner})
    rc = w3.eth.wait_for_transaction_receipt(tx)
    cf = w3.eth.contract(address=rc.contractAddress, abi=iface["abi"])
    print(f'\n=== Campaign: "{cf.functions.title().call()}" ===')
    print("Contract   :", rc.contractAddress)
    print("Goal       :", eth(cf.functions.goal().call()), "| Duration: 1 hour")
    print("Status     :", cf.functions.getStatus().call())
    return cf


def attempt(label, fn, sender, value=0):
    """Dry-run to catch revert reasons, then send the real transaction."""
    try:
        fn.call({"from": sender, "value": value})
    except Exception as e:
        reason = revert_reason(e)
        print(f'[REVERT] {label} -> "{reason}"')
        return
    rc = w3.eth.wait_for_transaction_receipt(fn.transact({"from": sender, "value": value}))
    print(f"[OK]     {label} (gas {rc.gasUsed})")


def time_travel(seconds):
    print(f"\n>> Time travel: +{seconds} seconds (deadline passed)")
    w3.provider.make_request("evm_increaseTime", [seconds])
    w3.provider.make_request("evm_mine", [])


# ---------- Scenario 1: goal reached ----------
cf = deploy("Build a Community Library", 5)
attempt("Donor A contributes 3 ETH", cf.functions.contribute(), donor_a, w3.to_wei(3, "ether"))
attempt("Donor B contributes 2.5 ETH", cf.functions.contribute(), donor_b, w3.to_wei(2.5, "ether"))
attempt("Donor C contributes 0 ETH", cf.functions.contribute(), donor_c, 0)
print("Raised     :", eth(cf.functions.totalRaised().call()),
      "| Contributors:", cf.functions.contributorsCount().call())
attempt("Owner withdraws before deadline", cf.functions.withdrawFunds(), owner)

time_travel(3601)
print("Status     :", cf.functions.getStatus().call())
attempt("Donor A contributes after deadline", cf.functions.contribute(), donor_a, w3.to_wei(1, "ether"))
attempt("Donor A requests refund (goal reached)", cf.functions.refund(), donor_a)
attempt("Non-owner withdraws", cf.functions.withdrawFunds(), donor_a)
before = w3.eth.get_balance(owner)
attempt("Owner withdraws funds", cf.functions.withdrawFunds(), owner)
after = w3.eth.get_balance(owner)
print("Owner balance increased by ~", w3.from_wei(after - before, "ether"), "ETH (after gas)")
print("Contract balance:", eth(w3.eth.get_balance(cf.address)))

# ---------- Scenario 2: goal failed -> refunds ----------
cf = deploy("Launch a Mobile App", 10)
attempt("Donor A contributes 2 ETH", cf.functions.contribute(), donor_a, w3.to_wei(2, "ether"))
attempt("Donor B contributes 1 ETH", cf.functions.contribute(), donor_b, w3.to_wei(1, "ether"))
print("Raised     :", eth(cf.functions.totalRaised().call()))

time_travel(3601)
print("Status     :", cf.functions.getStatus().call())
attempt("Owner withdraws (goal not reached)", cf.functions.withdrawFunds(), owner)
before = w3.eth.get_balance(donor_a)
attempt("Donor A refund", cf.functions.refund(), donor_a)
after = w3.eth.get_balance(donor_a)
print("Donor A refunded ~", w3.from_wei(after - before, "ether"), "ETH (after gas)")
attempt("Donor A refund again", cf.functions.refund(), donor_a)
