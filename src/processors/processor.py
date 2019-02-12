import os

from src.processors.yaml_processor import YAMLProcessor


class Processor:
	def __init__(self, search_path):
		self.search_path = search_path
		self.resources = {}
		self.yaml_processor = YAMLProcessor(self.resources)

	def process_files(self):
		for root, dirs, files in os.walk(self.search_path):
			for filename in files:
				if self.is_yaml(filename):
					self.yaml_processor.add_file_to_dictionary(root, filename)

		for key in self.yamls:
			locale = self.yamls[key]["locale"]
			if locale == "en":
				path = self.yamls[key]["path"]
				Processor.process_yaml(locale, path)

	@staticmethod
	def is_yaml(filename):
		if filename.endswith(".yml"):
			return True

		return False

	def vote_on_type(self, votes):
		final_vote = "UNKNOWN"
		for vote in votes:
			if vote in ["int", "float"]:
				if final_vote in ["UNKNOWN", "number"]:
					final_vote = "config_number"
			elif vote in ["list", "object"]:
				final_vote = "complex"
			elif vote in ["string"]:
				if final_vote in ["UNKNOWN", "number", "string"]:
					final_vote = "string"
			elif vote in ["config_string"]:
				if final_vote in ["UNKNOWN", "config_string"]:
					final_vote = "config_string"

		return final_vote

	def get_type_from_locale(self, value):
		if isinstance(value, int):
			return "int"
		elif isinstance(value, float):
			return "float"
		elif isinstance(value, list):
			return "array"
		elif isinstance(value, dict):
			return "object"
		elif isinstance(value, str):
			if len(value.split(" ")) == 1:
				return "config_string"
			return "string"
		else:
			return "UNKNOWN"
