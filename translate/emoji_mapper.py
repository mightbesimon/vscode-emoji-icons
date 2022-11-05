'''	Copyright © 2022 mightbesimon.com
	All rights reserved.

	Material belonging to others may have been
	used under Creative Commons Licence or with
	explicit or implicit permission.
'''

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from .models import IconType, ReferenceItem, IconItem

################################################################
#######                      class                       #######
################################################################
class EmojiMapper(ABC):

	@staticmethod
	def _text_to_references(icon_type:IconType, text:str) -> List[ReferenceItem]:
		return [
			ReferenceItem(icon_type, line)
			for line in text.split('\n')
			if line.startswith('-') and 'default' not in line
		]

	@staticmethod
	def _references_to_icons(references:List[ReferenceItem]) -> List[IconItem]:
		return [
			IconItem(
				icon_type=reference.icon_type,
				name=name,
				emoji=reference.emoji,
			)
			for reference in references
			for name in reference.names
		]

	@staticmethod
	def _references_to_json(references:List[ReferenceItem]):
		return ','.join(
			f'"{icon.name}":"{icon.emoji}"'
			for icon in EmojiMapper._references_to_icons(references)
		)

	@abstractmethod
	def all_emojis(self) -> List[str]:
		raise NotImplemented

	@abstractmethod
	def icon_theme(self) -> str:
		raise NotImplemented

	@abstractmethod
	def update_readme(self, filename:str=None) -> EmojiMapper:
		raise NotImplemented

	def export_icon_theme(self, filename:str=None) -> EmojiMapper:
		with open(filename, 'w') as file:
			file.write(self.icon_theme())

		return self
