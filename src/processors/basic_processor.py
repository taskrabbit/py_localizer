import re
import os


class BasicProcessor:
	LOCALE_PATTERN = re.compile("en[A-Z-]{0,3}")

	def __init__(self, search_path, resource_dict):
		self.search_path = search_path
		self.resource_dict = resource_dict

	def process(self, locale, path):
		pass

	@staticmethod
	def get_locale_from_file_path(path, fallback_locale):
		result = BasicProcessor.LOCALE_PATTERN.match(path)
		if result:
			str_locale = result.group(0)
		else:
			str_locale = fallback_locale

		return str_locale

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

	def get_locale_from_filename(self, filename):
		result = BasicProcessor.LOCALE_PATTERN.search(filename)
		if result:
			return result.group(0)
		else:
			return None

