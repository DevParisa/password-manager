import argparse
from vault import Vault
from getpass import getpass
from exceptions import FileSaveError, FileLoadError, VaultNotFoundError, InvalidPasswordError, VaultError

parser = argparse.ArgumentParser(description="Password Manager")
subparsers = parser.add_subparsers(dest="command", required=True)

subparsers.add_parser("init", help="Initialize a new vault")

add_pars = subparsers.add_parser("add", help="Add a password")
add_pars.add_argument("service", help="Service name")
add_pars.add_argument("password", help="Password to store")

get_parser = subparsers.add_parser("get", help="Get a password")
get_parser.add_argument("service", help="Service name")

subparsers.add_parser("list", help="List all services")


args = parser.parse_args()
#TODO create Session mode for better performance
# python main.py session
# Enter master password: ****
# vault> add gmail mypass
# vault> add twitter secret
# vault> list
# vault> save
# vault> exit

VAULT_FILE = "vault.dat"

if args.command == "init":
    # create new vault
    if Vault.exists(VAULT_FILE):
    	print("Vault already exists")
    else:
    	master_password = getpass("Create master password: ")
    	vault = Vault()
    	vault.save_file(VAULT_FILE, master_password)
    	print("Vault created.")

elif args.command == "add":
	# load vault, add password, save vault
	try:
		master_password = getpass("Enter master password: ")
		vault = Vault()
		vault.load_file(VAULT_FILE, master_password)
		vault.add(args.service, args.password)
		vault.save_file(VAULT_FILE, master_password)
		print(f"Added {args.service}.")
	except VaultNotFoundError:
		print("Run 'python main.py init' first.")
	except InvalidPasswordError:
		print("Wrong password. Try again.")
	except ValueError as e:
		print(f"Error: {e}")

elif args.command == "get":
	# load vault, get password, print it
	try:
		master_password = getpass("Enter master password: ")
		vault = Vault()
		vault.load_file(VAULT_FILE, master_password)
		print(vault.get(args.service))
	except VaultNotFoundError:
		print("Run 'python main.py init' first.")
	except InvalidPasswordError:
		print("Wrong password. Try again.")
	except KeyError:
		print(f"Service '{args.service}' not found.")

elif args.command == "list":
	# load vault, list services
	try:
		master_password = getpass("Enter master password: ")
		vault = Vault()
		vault.load_file(VAULT_FILE, master_password)
		services = vault.list_services()
		if services:
			for s in services:
				print(f"	-{s}")
		else:
			print("No services stored yet.")
	except VaultNotFoundError:
		print("Run 'python main.py init' first.")
	except InvalidPasswordError:
		print("Wrong password. Try again.")