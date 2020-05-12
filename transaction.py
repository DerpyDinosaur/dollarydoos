# Imports
from tools import *

# Functions
""" Welcome fucntion that clears the screen and places banner """
def welcome():
	clearScreen()

	width = 35
	print("-"*width)
	print("Dollarydoos Transactions".center(width))
	print("-"*width)

#///////////////////////////////////////////////////////////

# TODO: Add a read ledger option
# Variables
init = True
signal.signal(signal.SIGINT, handler)

# Main
while True:
	if init:
		welcome()
		init = False

	print("\n[N] New transaction")
	print("[D] Delete ledger")
	print("[Q] Quit program")
	choice = input("\nSelect an option: ").lower()

	if choice in ['n', 'new']:
		BlockChain.newTransaction()
		init = True

	elif choice in ['d', 'delete']:
		deleteFile('ledger')

	elif choice in ['q', 'quit']:
		exit()

	else:
		print("\""+choice+"\"", "Is not an option.")