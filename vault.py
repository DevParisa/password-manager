from crypto import derive_key, encrypt_data, decrypt_data
import os
import json
from exceptions import FileSaveError, FileLoadError, VaultNotFoundError, InvalidPasswordError, VaultError
from cryptography.fernet import InvalidToken

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

	def update(self, service, new_password):
		if service not in self.dvault:
			raise KeyError(f"Service '{service}' not found")
		self.dvault[service] = new_password

	def delete(self, service):
		if service not in self.dvault:
			raise KeyError(f"Service '{service}' not found")
		del self.dvault[service]

	def save_file(self, filepath: str, master_password: str):
		salt = os.urandom(16)
		key = derive_key(master_password, salt)
		encrypted = encrypt_data(json.dumps(self.dvault), key)

		temp_filepath = filepath + ".tmp"
		try:
			# Write to temp file first
			with open(temp_filepath, "wb") as file:
				file.write(salt+encrypted) #salt is alwasy 16 bytes
			# Only replace original if write succeeded
			os.replace(temp_filepath, filepath)  # atomic on most systems, it moves the temp file to become the real file 
		except Exception as e:
			if os.path.exists(temp_filepath):
				os.remove(temp_filepath)
			raise FileSaveError(f"Error saving file: {e}")
			

	def load_file(self, filepath: str, master_password: str):
		if not os.path.exists(filepath):
			raise VaultNotFoundError("Vault not found")
		try:
			with open(filepath, "rb") as file:
				data = file.read()
			salt = data[:16]
			key = derive_key(master_password, salt)
			data_str = decrypt_data(data[16:], key)
			self.dvault = json.loads(data_str)
		except InvalidToken:
			raise InvalidPasswordError("Wrong master password.")
		except Exception as e:
			raise FileLoadError(f"Error loading file: {e}")
			

	@staticmethod
	def exists(filepath: str) -> bool:
		return os.path.exists(filepath)