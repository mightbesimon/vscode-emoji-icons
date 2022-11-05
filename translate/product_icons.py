'''	Copyright © 2022 mightbesimon.com
	All rights reserved.

	Material belonging to others may have been
	used under Creative Commons Licence or with
	explicit or implicit permission.
'''

from __future__ import annotations
from typing import List

from .models import IconType, ReferenceItem
from .emoji_mapper import EmojiMapper

################################################################
#######                      class                       #######
################################################################
class ProductIconMapper(EmojiMapper):

	def __init__(self, filename:str) -> None:
		self.filename: str = filename
		self.icons: List[ReferenceItem] = []
		self._parse_data()

	def _parse_data(self) -> None:
		with open(self.filename, 'r') as file:
			content = file.read()

		self.icons = EmojiMapper._text_to_references(
			IconType.file_extension, content)

	def all_emojis(self) -> List[str]:
		return sorted(list(set(
			reference.emoji
			for reference in self.icons
		)))

	def icon_theme(self) -> str:
		fonts = (
			'"id":"emoji-apple",'
			'"style":"normal",'
			'"weight":"normal",'
			'"src":[{'
				'"path":"",'
				'"format":"truetype"'
			'}]'
		)

		icon_definitions = ','.join(
			f'"{icon.name}":{{"fontCharacter":"{icon.emoji}"}}'
			for icon in EmojiMapper._references_to_icons(self.icons)
		)

		return (
			'{'
				f'"fonts":[{{{fonts}}}],'
				f'"iconDefinitions":{{{icon_definitions}}}'
			'}'
		)

	def update_readme(self, filename:str='README.md') -> ProductIconMapper:
		with open(filename, 'r') as file:
			readme = file.read()

		with open(self.filename, 'r') as file:
			emoji_reference = file.read()

		with open(filename, 'w') as file:
			file.write(
				readme + '\n' + emoji_reference
			)

		return self
