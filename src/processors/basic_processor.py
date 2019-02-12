import re
import os


class BasicProcessor:
	LOCALE_PATTERN = re.compile("en[A-Z-]{0,3}")

	def __init__(self, resource_dict):
		self.resource_dict = resource_dict

	def process(self):
		pass

	@staticmethod
	def get_locale_from_file_path(path, fallback_locale):
		result = BasicProcessor.LOCALE_PATTERN.match(path)
		if result:
			str_locale = result.group(0)
		else:
			str_locale = fallback_locale

		return str_locale

