import hashlib
import time


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = (
            str(self.index)
            + str(self.timestamp)
            + str(self.data)
            + str(self.previous_hash)
            + str(self.nonce)
        )
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        start = time.time()
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        elapsed = time.time() - start
        print(f"Block {self.index} mined | Nonce: {self.nonce} "
              f"| Time: {elapsed:.4f}s")
        print(f"Hash: {self.hash}")


class Blockchain:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), data, previous_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        target = "0" * self.difficulty
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
            if current.hash[:self.difficulty] != target:
                return False
        return True


# Create blockchain with difficulty 4 (hash must start with "0000")
print("Mining blocks with difficulty = 4")
print("=" * 60)
blockchain = Blockchain(difficulty=4)
blockchain.add_block("Transaction 1: Alice -> Bob")
blockchain.add_block("Transaction 2: Bob -> Charlie")
blockchain.add_block("Transaction 3: Charlie -> David")

# Display blockchain
print("\nBlockchain:")
for block in blockchain.chain:
    print("-" * 60)
    print("Block:", block.index)
    print("Data:", block.data)
    print("Nonce:", block.nonce)
    print("Hash:", block.hash)
    print("Previous Hash:", block.previous_hash)
print("-" * 60)

print("Blockchain Valid:", blockchain.is_chain_valid())

# Effect of difficulty on mining time
print("\nDifficulty vs Mining Time")
print("Difficulty | Nonce      | Time (s)")
for d in range(1, 6):
    b = Block(1, "Test Transaction", "0")
    start = time.time()
    target = "0" * d
    while b.hash[:d] != target:
        b.nonce += 1
        b.hash = b.calculate_hash()
    print(f"{d:<10} | {b.nonce:<10} | {time.time() - start:.4f}")

# Tamper with a block
blockchain.chain[1].data = "Tampered Transaction"
print("\nAfter tampering:")
print("Blockchain Valid:", blockchain.is_chain_valid())
