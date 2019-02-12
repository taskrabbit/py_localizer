from src.processors.basic_processor import BasicProcessor

import os
import yaml
import json


class YAMLProcessor(BasicProcessor):
	def __init__(self, resource_dict):
		BasicProcessor.__init__(self, resource_dict)
		self.flat_dict = {}

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
		for key, value in self.flat_dict.items():
			print("{}".format("="*100))
			print("key: {}".format(key))
			for locale_key, locale_value in value.items():
				print("\t{} : {}".format(locale_key, locale_value))

		fh = open('resources.json', 'w')
		fh.write(json.dumps(self.flat_dict))
		fh.close()

	def set_key_value_types(self):
		for key, value in self.flat_dict.items():
			type_votes = []
			for locale_key, locale_value in value.items():
				if locale_key != "type":
					type_votes.append(Main.get_type_from_locale(locale_value))

			value["type"] = Main.vote_on_type(type_votes)

	def get_keys_from_dict(self, locale, str_path, key, value):
		if len(str_path) > 0:
			str_path = "{}.{}".format(str_path, key)
		else:
			str_path = key

		if isinstance(value, list):
			for i in range(0, len(value)):
				self.get_keys_from_dict(locale, "{}.index_{}".format(str_path, i), key, value[0])

		elif not isinstance(value, dict):
			if str_path not in self.flat_dict:
				self.flat_dict[str_path] = {
					"type": "UNKNOWN"
				}
			entry_dict = self.flat_dict[str_path]
			entry_dict[locale] = value
		else:
			for key, value in value.items():
				self.get_keys_from_dict(locale, str_path, key, value)

	def add_file_to_dictionary(self, root, filename):
		locale = Main.get_locale_from_filename(filename)
		path = os.path.join(root, filename)
		file_obj = {
			"filename": filename,
			"locale": locale,
			"path": path
		}
		self.yamls[path] = file_obj