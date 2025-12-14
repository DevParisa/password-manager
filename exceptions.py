class VaultError(Exception):
	# Base exception for vault errors
	pass

class FileLoadError(VaultError):
	pass

class FileSaveError(VaultError):
	pass

class VaultNotFoundError(VaultError):
	pass

class InvalidPasswordError(VaultError):
	pass