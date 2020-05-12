# Imports
import time
from tools import *

#//////////////////////////////////////////////////////
# Variables
nonce = 50001
difficulty = 14

# Main
while True:
	if nonce == 50001:
		time.sleep(2)

		block = BlockChain()
		if not BlockChain.newBlock(block):
			clearScreen()
			print("Awaiting new transaction...")
			print("Ctrl + C to quit")
			continue

		nonce = 0

	block.newBlock['timestamp'] = date.strftime("%H:%M:%S %d-%b-%Y")
	block.newBlock['nonce'] = nonce

	# Compute hash for block
	block.setHash()
	print(block.currentHash[:difficulty], ":", nonce)

	if block.currentHash[:difficulty] == difficulty*"0" or nonce == 50000:
		block.newBlock['hash'] = block.currentHash
		block.chain.append(block.newBlock)
		writeToFile(block.chain, 'blockchain')
	
	nonce = nonce + 1