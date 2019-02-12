import os

from src.utils.environment import Environment

from src.processors.processor import Processor


class Main:
	ENGINES_LOCALTION = "/Users/markweaver/projects/taskrabbit/v3/apps"

	def __init__(self, engine_name=None):
		self.engine_name = engine_name

		self.repo_root = Environment("dev").get_value("v3_path")

		if not self.engine_name:
			raise LookupError()

		self.engine_path = self.repo_root + "/" + self.engine_name
		if not os.path.isdir(self.engine_path):
			raise AttributeError()

		self.processor = Processor(self.engine_path)

	def run(self):
		self.processor.process_files()

		self.processor.print_output()


if __name__ == "__main__":
	main = Main("organic")
	main.run()