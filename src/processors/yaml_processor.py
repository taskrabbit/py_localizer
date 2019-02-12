from src.processors.basic_processor import BasicProcessor

import os
import yaml
import json


class YAMLProcessor(BasicProcessor):
	def __init__(self, search_path, resource_dict):
		BasicProcessor.__init__(self, search_path, resource_dict)
		self.resource_dict = resource_dict
		self.yamls = {}

	def process(self, locale, path):
		yaml_file = None

		with open(path, 'r') as stream:
			try:
				yaml_file = yaml.load(stream)
			except yaml.YAMLError as e:
				print(e)

		for key, value in yaml_file.items():
			str_locale = BasicProcessor.get_locale_from_file_path(key, locale)

			self.get_keys_from_dict(str_locale, "", "", value)

		self.set_key_value_types()

	def print_yamls(self):
		for key, value in self.resource_dict.items():
			print("{}".format("="*100))
			print("key: {}".format(key))
			for locale_key, locale_value in value.items():
				print("\t{} : {}".format(locale_key, locale_value))

		fh = open('resources.json', 'w')
		fh.write(json.dumps(self.resource_dict))
		fh.close()

	def set_key_value_types(self):
		for key, value in self.resource_dict.items():
			type_votes = []
			for locale_key, locale_value in value.items():
				if locale_key != "type":
					type_votes.append(self.get_type_from_locale(locale_value))

			value["type"] = self.vote_on_type(type_votes)

	def get_keys_from_dict(self, locale, str_path, key, value):
		if len(str_path) > 0:
			str_path = "{}.{}".format(str_path, key)
		else:
			str_path = key

		if isinstance(value, list):
			for i in range(0, len(value)):
				self.get_keys_from_dict(locale, "{}.index_{}".format(str_path, i), key, value[0])

		elif not isinstance(value, dict):
			if str_path not in self.resource_dict:
				self.resource_dict[str_path] = {
					"type": "UNKNOWN"
				}
			entry_dict = self.resource_dict[str_path]
			entry_dict[locale] = value
		else:
			for key, value in value.items():
				self.get_keys_from_dict(locale, str_path, key, value)

	def add_file_to_dictionary(self, root, filename):
		locale = self.get_locale_from_filename(filename)
		path = os.path.join(root, filename)
		file_obj = {
			"filename": filename,
			"locale": locale,
			"path": path
		}
		self.yamls[path] = file_obj

	def process_files(self):
		for root, dirs, files in os.walk(self.search_path):
			for filename in files:
				if self.is_yaml(filename):
					self.add_file_to_dictionary(root, filename)

		for key in self.yamls:
			locale = self.yamls[key]["locale"]
			if locale == "en":
				print("path: {}".format(self.search_path))
				path = self.yamls[key]["path"]
				self.process(locale, path)

	def is_yaml(self, filename):
		if filename.endswith(".yml"):
			return True

		return False