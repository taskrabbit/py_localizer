import configparser


class Environment:
	CONFIG_PATH = "../config/environments.cfg"
	_instance = None

	def __init__(self, env):
		if Environment._instance is None:
			Environment._instance = self
			self.env = env
			self.config = configparser.ConfigParser()
			self.config.read(Environment.CONFIG_PATH)

	@staticmethod
	def get_value(key):
		if Environment._instance is None:
			return Environment._instance.get_value(key)

	def get_value(self, key):
		return self.config[self.env][key]



