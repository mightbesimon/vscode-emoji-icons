'''	Copyright © 2022 mightbesimon.com
	All rights reserved.

	Material belonging to others may have been
	used under Creative Commons Licence or with
	explicit or implicit permission.
'''

from dataclasses import dataclass
from enum import Enum
from typing import List

################################################################
#######                      enums                       #######
################################################################
class IconType(Enum):
	file_extension = 'fileExtensions'
	file_name      = 'fileNames'
	folder_name   = 'folderNames'

################################################################
#######                   dataclasses                    #######
################################################################
@dataclass
class ReferenceItem:
	icon_type: IconType
	emoji: str
	names: List[str]
	comment: str

	def __init__(self, icon_type:IconType, text:str):
		self.icon_type = icon_type
		text = text[2:]
		self.emoji, text = text.split(' ', 1)
		names, *comment = text.split(' (')
		self.names = names.split(' / ')
		self.comment = comment[0].rstrip(')') if comment else None

		if icon_type == IconType.file_extension:
			self.names = [ name.lstrip('.') for name in self.names ]

@dataclass
class IconItem:
	icon_type: IconType
	name: str
	emoji: str

################################################################
#######                      class                       #######
################################################################
class EmojiReference:

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
			f'"{file_extension.name}":"{file_extension.emoji}"'
			for file_extension in EmojiReference._references_to_icons(references)
		)

	def __init__(self, filename:str):
		self.filename: str = filename
		self.file_extensions: List[ReferenceItem] = []
		self.file_names     : List[ReferenceItem] = []
		self.folder_names  : List[ReferenceItem] = []
		self._parse_data()

	def _parse_data(self) -> None:
		with open(self.filename, 'r') as file:
			content = file.read()

		content = content[content.index('\n\n')+2:-1]
		file_names, content = content.split('\n\n### File Extensions\n\n')
		file_extensions, folder_names = content.split('\n\n### Folders\n\n')

		self.file_extensions = EmojiReference._text_to_references(
			IconType.file_extension, file_extensions)

		self.file_names = EmojiReference._text_to_references(
			IconType.file_name, file_names)

		self.folder_names = EmojiReference._text_to_references(
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

		file_extensions = EmojiReference._references_to_json(self.file_extensions)
		file_names = EmojiReference._references_to_json(self.file_names)
		folder_names = EmojiReference._references_to_json(self.folder_names)

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

	def export_icon_theme(self, filename:str=None) -> 'EmojiReference':
		filename = filename if filename else 'file-icons/emoji-icon-theme.json'

		with open(filename, 'w') as file:
			file.write(self.icon_theme())

		return self

	def update_readme(self, filename:str=None) -> 'EmojiReference':
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


################################################################
#######                 MAIN STARTS HERE                 #######
################################################################
if __name__ == '__main__':
	(
		EmojiReference(filename='file-icons/emoji-reference.md')
			.export_icon_theme()
			.update_readme()
	)
