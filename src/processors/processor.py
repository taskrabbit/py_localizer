import os
import json

from src.processors.yaml_processor import YAMLProcessor


class Processor:
	def __init__(self, search_path):
		self.resources = {}
		self.yaml_processor = YAMLProcessor(search_path, self.resources)

	def process_files(self):
		self.yaml_processor.process_files()

	def print_output(self):
		for key, value in self.resources.items():
			print("{}".format("="*100))
			print("key: {}".format(key))
			for locale_key, locale_value in value.items():
				print("\t{} : {}".format(locale_key, locale_value))

	def save_json_output(self):
		fh = open('resources.json', 'w')
		fh.write(json.dumps(self.resources))
		fh.close()
