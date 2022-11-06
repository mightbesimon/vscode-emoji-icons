'''	Copyright © 2022 mightbesimon.com
	All rights reserved.

	Material belonging to others may have been
	used under Creative Commons Licence or with
	explicit or implicit permission.
'''

from __future__ import annotations
from typing import Dict, List

from .models import IconType, ReferenceItem
from .emoji_mapper import EmojiMapper

################################################################
#######                      class                       #######
################################################################
class FileIconMapper(EmojiMapper):

	def __init__(self) -> None:
		self.reference_contents: List[str] = []
		self.references: Dict[IconType, List[ReferenceItem]] = {
			IconType.extension : [],
			IconType.file      : [],
			IconType.folder    : [],
		}

	def load_reference(self, filename: str, icon_type: IconType) -> FileIconMapper:
		with open(filename, 'r') as file:
			content = file.read()

		self.reference_contents.append(content)
		self.references[icon_type] += (EmojiMapper
			._text_to_references(icon_type, content))

		return self

	def all_emojis(self) -> List[str]:
		return sorted(
			list( set( reference.emoji
				for references in self.references.values()
				for reference in references
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

		json = {
			icon_type: EmojiMapper._references_to_json(references)
			for icon_type, references in self.references.items()
		}

		icon_definitions = ','.join(
			f'"{emoji}":{{"fontCharacter":"{emoji}","fontSize":"125%"}}'
			for emoji in self.all_emojis()
		)

		return (
			'{'
				f'{defaults}'
				f'"fileExtensions":{{{json[IconType.extension]}}},'
				f'"fileNames":{{{json[IconType.file]}}},'
				f'"folderNames":{{{json[IconType.folder]}}},'
				f'"folderNamesExpanded":{{{json[IconType.folder]}}},'
				f'"iconDefinitions":{{{icon_definitions}}}'
			'}'
		)

	def update_readme(self, filename:str='README.md') -> FileIconMapper:
		with open(filename, 'r') as file:
			readme = file.read()

		with open(filename, 'w') as file:
			file.write(
				readme[:readme.index('### Special Files\n\n')]
				+ '\n'.join(self.reference_contents)
			)

		return self
