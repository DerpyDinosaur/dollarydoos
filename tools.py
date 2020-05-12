import signal
import datetime
import json
import hashlib
import os

# Globals
date = datetime.datetime.now()

""" If signal interrupt has occured, program will terminate """
def handler(signum, frame):
    print("\nTerminating Program...")
    exit()
signal.signal(signal.SIGINT, handler)

def clearScreen():
	if os.system("cls") == 0:
		# Windows
		os.system("cls")
	else:
		# Linux
		os.system("clear")

""" Write data to file """ 
def writeToFile(data, filename):
	try:
		with open(filename,'w') as file:
			json.dump(data, file, indent=4) 
	except:
		print("An error has occured while writing to a file...")
		return False

""" Clean slate the ledger """
def deleteFile(filename):
	choice = input("Are you sure, [Yes] or [No]: ").lower()

	if not choice in ['y', 'yes']:
		print("\nLedger was not deleted.")
		return

	file = open(filename, 'w')
	file.close()
	print("\nLedger has been cleared.")

""" Class storage for the blockchain """
class BlockChain:
	def __init__(self):
		currentHash = ""
		blockZero = {
			"index": 0,
			"timestamp": date.strftime("%H:%M:%S %d-%b-%Y"),
			"data": "first block",
			"hash": "2af7909ca08f18facc556624b02e1a5c683bb0f557137b1ef7e0028fc457715c",
			"nonce": 0
		}

		try:
			with open('blockchain', 'r') as file:
				self.chain = json.load(file)
				self.chain[0]['index'] = 0 
		except:
			self.chain = [blockZero]
			writeToFile(self.chain, 'blockchain')

		self.newBlock = {
			"index": None,
			"timestamp": None,
			"data": None,
			"hash": None,
			"nonce": None
		}

	def newBlock(self):
		try:
			with open('ledger', 'r') as file:
				oldData = json.load(file)
				oldData[0] = oldData[0]
		except:
			print("[x] Empty or unreadable ledger file.")
			return False

		if oldData == self.chain[-1]['data'] or oldData == "first block":
			return False

		self.newBlock['index'] = self.chain[-1]['index'] + 1
		self.newBlock['data'] = oldData
		self.newBlock['hash'] = self.chain[-1]['hash']
		return True

	def setHash(self):
		self.currentHash = hashlib.sha256()
		self.currentHash.update(str(self.newBlock['index']).encode('utf8'))
		self.currentHash.update(str(self.newBlock['timestamp']).encode('utf8'))
		self.currentHash.update(str(self.newBlock['data']).encode('utf8'))
		self.currentHash.update(str(self.chain[-1]['hash']).encode('utf8'))
		self.currentHash.update(str(self.newBlock['nonce']).encode('utf8'))
		self.currentHash = self.currentHash.hexdigest()
		return self.currentHash

	def newTransaction():
		filename = 'ledger'
		newData = {
			"timestamp": None,
			"sender": None,
			"reciever": None,
			"amount": None
		}

		try:
			with open(filename, 'r') as file:
				oldData = json.load(file)
		except:
			oldData = []
			file = open(filename, 'w')
			file.close()

		while True:
			newData['sender'] = input("\nWho is the sender: ").strip().capitalize()
			newData['reciever'] = input("Who is the reciever: ").strip().capitalize()
			# Test if input was a number
			try:
				newData['amount'] = int(input("How much will be transfered: "))
			except:
				print("[x] The amount needs to be a number.")
				continue

			# Check if the user has inputed incorrectly
			if newData['sender'] == "" or newData['reciever'] == "" or newData['sender'] == newData['reciever']:
				print("[x] One of the entries was invalid.")
				continue

			print("\n"+newData['sender'], "->", newData['reciever'], ":", newData['amount'], "Dollarydoos")
			isComplete = input("Is the above correct, [Yes] or [No]: ").lower()
			if isComplete in ['y', 'yes']: break

		newData['timestamp'] = date.strftime("%H:%M:%S %d-%b-%Y")
		oldData.append(newData)

		writeToFile(oldData, filename)
		