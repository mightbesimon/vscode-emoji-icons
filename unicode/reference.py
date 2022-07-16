'''	Copyright © 2022 mightbesimon.com
	All rights reserved.

	Material belonging to others may have been
	used under Creative Commons Licence or with
	explicit or implicit permission.
'''

from dataclasses import dataclass
from enum import Enum
from turtle import width
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
		file_names, content = content.split('\n\nfile extensions\n\n')
		file_extensions, folder_names = content.split('\n\nfolders\n\n')

		self.file_extensions = [
			ReferenceItem(IconType.file_extension, file_extension)
			for file_extension in file_extensions.split('\n')[1:]
		]
		self.file_names = [
			ReferenceItem(IconType.file_name, file_name)
			for file_name in file_names.split('\n')
		]
		self.folder_names = [
			ReferenceItem(IconType.folder_name, folder_name)
			for folder_name in folder_names.split('\n')[1:]
		]

	@staticmethod
	def references_to_icons(references:List[ReferenceItem]) -> List[IconItem]:
		return [
			IconItem(
				icon_type=reference.icon_type,
				name=name,
				emoji=reference.emoji,
			)
			for reference in references
			for name in reference.names
		]

	def all_emojis(self) -> List[str]:
		return sorted( list( set( reference.emoji for reference in
			self.file_extensions + self.file_names + self.folder_names
		)))

	def icon_theme(self) -> str:
		defaults = (
			'"showLanguageModeIcons":true,'
			'"folder": "📁",'
			'"folderExpanded": "📂",'
			'"file": "📄",'
		)
		file_extensions = ','.join(
			f'"{file_extension.name}":"{file_extension.emoji}"'
			for file_extension in EmojiReference.references_to_icons(self.file_extensions)
		)
		file_names = ','.join(
			f'"{file_name.name}":"{file_name.emoji}"'
			for file_name in EmojiReference.references_to_icons(self.file_names)
		)
		folder_names = ','.join(
			f'"{folder_name.name}":"{folder_name.emoji}"'
			for folder_name in EmojiReference.references_to_icons(self.folder_names)
		)
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

	def update_readme(self, filename:str=None):
		filename = filename if filename else 'README.md'

		with open(filename, 'r') as file:
			readme = file.read()

		with open(self.filename, 'r') as file:
			emoji_reference = file.read()

		with open(filename, 'w') as file:
			file.write(
				readme[:readme.index('special files\n\n')]
				+ emoji_reference
			)


################################################################
#######                 MAIN STARTS HERE                 #######
################################################################
if __name__ == '__main__':
	(
		EmojiReference(filename='file-icons/emoji-reference.md')
			.export_icon_theme()
			.update_readme()
	)
