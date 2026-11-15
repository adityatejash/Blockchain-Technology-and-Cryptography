import hashlib


def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()


class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.levels = []
        self.root = self.build_tree()

    def build_tree(self):
        level = [sha256(tx) for tx in self.transactions]
        self.levels.append(level)
        while len(level) > 1:
            # Duplicate last hash if the number of nodes is odd
            if len(level) % 2 == 1:
                level = level + [level[-1]]
            next_level = []
            for i in range(0, len(level), 2):
                next_level.append(sha256(level[i] + level[i + 1]))
            level = next_level
            self.levels.append(level)
        return level[0]

    def get_proof(self, index):
        """Return the sibling hashes needed to verify a transaction."""
        proof = []
        for level in self.levels[:-1]:
            nodes = level + [level[-1]] if len(level) % 2 == 1 else level
            sibling = index ^ 1
            position = "left" if sibling < index else "right"
            proof.append((nodes[sibling], position))
            index //= 2
        return proof


def verify_proof(transaction, proof, root):
    current = sha256(transaction)
    for sibling, position in proof:
        if position == "left":
            current = sha256(sibling + current)
        else:
            current = sha256(current + sibling)
    return current == root


transactions = [
    "Alice -> Bob: 10",
    "Bob -> Charlie: 5",
    "Charlie -> David: 3",
    "David -> Eve: 2",
    "Eve -> Frank: 1",
]

tree = MerkleTree(transactions)

# Display tree
print("Merkle Tree Levels (leaf level first)")
for n, level in enumerate(tree.levels):
    print(f"\nLevel {n}:")
    for h in level:
        print("  ", h[:32] + "...")
print("\nMerkle Root:", tree.root)

# Verify a transaction using Merkle proof
index = 2
tx = transactions[index]
proof = tree.get_proof(index)
print(f"\nVerifying transaction: '{tx}'")
for i, (h, pos) in enumerate(proof):
    print(f"  Proof step {i + 1}: {pos:<5} sibling = {h[:24]}...")
print("Transaction Verified:", verify_proof(tx, proof, tree.root))

# Verify a tampered transaction
fake = "Charlie -> David: 300"
print(f"\nVerifying tampered transaction: '{fake}'")
print("Transaction Verified:", verify_proof(fake, proof, tree.root))

# Tamper with data and recompute the root
transactions[0] = "Alice -> Bob: 1000"
print("\nRoot after tampering with transaction 1:")
print(MerkleTree(transactions).root)
print("Root unchanged:", MerkleTree(transactions).root == tree.root)
