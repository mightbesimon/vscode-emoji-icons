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
class FileIconMapper(EmojiMapper):

	EXPORT_FILENAME: str = 'file-icons/emoji-icon-theme.json'

	def __init__(self, filename:str) -> None:
		self.filename: str = filename
		self.file_extensions: List[ReferenceItem] = []
		self.file_names     : List[ReferenceItem] = []
		self.folder_names   : List[ReferenceItem] = []
		self._parse_data()

	def _parse_data(self) -> None:
		with open(self.filename, 'r') as file:
			content = file.read()

		content = content[content.index('\n\n')+2:-1]
		file_names, content = content.split('\n\n### File Extensions\n\n')
		file_extensions, folder_names = content.split('\n\n### Folders\n\n')

		self.file_extensions = EmojiMapper._text_to_references(
			IconType.file_extension, file_extensions)

		self.file_names = EmojiMapper._text_to_references(
			IconType.file_name, file_names)

		self.folder_names = EmojiMapper._text_to_references(
			IconType.folder_name, folder_names)

	def all_emojis(self) -> List[str]:
		return sorted(
			list( set( reference.emoji for reference in
				self.file_extensions + self.file_names + self.folder_names
			))
			+ ['📄', '📁', '📂']
		)

	def icon_theme(self) -> str:
		defaults = (
			'"showLanguageModeIcons":true,'
			'"file": "📄",'
			'"folder": "📁",'
			'"folderExpanded": "📂",'
		)

		file_extensions = EmojiMapper._references_to_json(self.file_extensions)
		file_names = EmojiMapper._references_to_json(self.file_names)
		folder_names = EmojiMapper._references_to_json(self.folder_names)

		icon_definitions = ','.join(
			f'"{emoji}":{{"fontCharacter":"{emoji}","fontSize":"125%"}}'
			for emoji in self.all_emojis()
		)

		return (
			'{'
				f'{defaults}'
				f'"fileExtensions":{{{file_extensions}}},'
				f'"fileNames":{{{file_names}}},'
				f'"folderNames":{{{folder_names}}},'
				f'"folderNamesExpanded":{{{folder_names}}},'
				f'"iconDefinitions":{{{icon_definitions}}}'
			'}'
		)

	def update_readme(self, filename:str=None) -> EmojiMapper:
		filename = filename if filename else 'README.md'

		with open(filename, 'r') as file:
			readme = file.read()

		with open(self.filename, 'r') as file:
			emoji_reference = file.read()

		with open(filename, 'w') as file:
			file.write(
				readme[:readme.index('### Special Files\n\n')]
				+ emoji_reference
			)

		return self
