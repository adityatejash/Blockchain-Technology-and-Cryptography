import hashlib
import time


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = (
            str(self.index)
            + str(self.timestamp)
            + str(self.data)
            + str(self.previous_hash)
        )
        return hashlib.sha256(block_data.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def add_block(self, data):
        previous_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            data,
            previous_block.hash
        )

        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check if current block was modified
            if current.hash != current.calculate_hash():
                return False

            # Check if blocks are properly linked
            if current.previous_hash != previous.hash:
                return False

        return True


# Create blockchain
blockchain = Blockchain()

# Add blocks
blockchain.add_block("Transaction 1: Alice -> Bob")
blockchain.add_block("Transaction 2: Bob -> Charlie")
blockchain.add_block("Transaction 3: Charlie -> David")

# Display blockchain
for block in blockchain.chain:
    print("Block:", block.index)
    print("Data:", block.data)
    print("Hash:", block.hash)
    print("Previous Hash:", block.previous_hash)
    print("-" * 50)

# Verify blockchain
print("Blockchain Valid:", blockchain.is_chain_valid())

# Tamper with a block
blockchain.chain[1].data = "Tampered Transaction"

print("\nAfter tampering:")
print("Blockchain Valid:", blockchain.is_chain_valid())