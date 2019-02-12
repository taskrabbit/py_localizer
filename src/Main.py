from src.processors.processor import Processor

import os


class Main:
	ENGINES_LOCALTION = "/Users/markweaver/projects/taskrabbit/v3/apps"

	def __init__(self, engine_name=None):
		self.engine_name = engine_name

		if not self.engine_name:
			raise LookupError()

		self.engine_path = Main.ENGINES_LOCALTION + "/" + self.engine_name
		if not os.path.isdir(self.engine_path):
			raise AttributeError()

		self.processor = Processor(self.engine_path)

	def run(self):
		for root, dirs, files in os.walk(self.engine_path):
			for filename in files:
				if self.is_yaml(filename):
					self.add_file_to_dictionary(root, filename)

		for key in self.yamls:
			locale = self.yamls[key]["locale"]
			if locale == "en":
				path = self.yamls[key]["path"]
				self.process_yaml(locale, path)

		self.print_yamls()

	@staticmethod
	def get_locale_from_filename(filename):
		result = Main.LOCALE_PATTERN.search(filename)
		if result:
			return result.group(0)
		else:
			return None


if __name__ == "__main__":
	main = Main("organic")
	main.run()