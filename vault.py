from crypto import derive_key, encrypt_data, decrypt_data
import os

class Vault:
	def __init__(self):
		self.dvault = {} # empty dictionary


	def add(self, service, password):
		if service in self.dvault:
			raise ValueError(f"Service '{service}' already exists")
		self.dvault[service] = password

	def get(self, service):
		if service not in self.dvault:
			raise KeyError(f"Service '{service}' not found")
		return self.dvault[service]

	def list_services(self):
		return list(self.dvault.keys())

	def save_file(self, filepath: str, master_password: str):
		salt = os.urandom(16)
		key = derive_key(master_password, salt)
		encrypted = encrypt_data(json.dumps(self.dvault), key)
		try:
			with open(filepath, "wb") as file:
				file.write(salt+encrypted) #salt is alwasy 16 bytes
		except Exception as e:
			raise FileSaveError(f"Error saving file: {e}")
			#FIXME catch specific exceptions separately—wrong password vs file not found vs corrupted file

	def load_file(self, filepath: str, master_password: str):
		try:
			with open(filepath, "rb") as file:
				data = file.read()
			salt = data[:16]
			key = derive_key(master_password, salt)
			data_str = decrypt_data(data[16:], key)
			self.dvault = json.loads(data_str)
		except Exception as e:
			raise FileLoadError(f"Error loading file: {e}")
			#FIXME catch specific exceptions separately—wrong password vs file not found vs corrupted file


# vault = Vault()
# try:
# 	vault.add("gmail", "mypassword")
# 	vault.add("gmail2", "mypassword2")
# 	print(vault.get("gmail3"))
# 	print(vault.list_services())
# except ValueError as e:
# 	print(f"cannot override {e}")
# except KeyError as e:
# 	print(f"key does not exists {e}")