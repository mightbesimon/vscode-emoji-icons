'''	Copyright © 2022 mightbesimon.com
	All rights reserved.

	Material belonging to others may have been
	used under Creative Commons Licence or with
	explicit or implicit permission.
'''

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

################################################################
#######                      enums                       #######
################################################################
class EmojiStatus(Enum):
	component  = 'component'
	fully      = 'fully-qualified'
	minimally  = 'minimally-qualified'
	unqualified = 'unqualified'

################################################################
#######                   dataclasses                    #######
################################################################
@dataclass
class Emoji:
	name: str
	emoji: str
	unicode: List[str]
	status: EmojiStatus
	version: str

	def __init__(self, text: str):
		unicode, text = text.split('; ')
		self.unicode = unicode.strip().split(' ')
		status, text = text.split('# ')
		self.status = EmojiStatus(status.strip())
		self.emoji, version, self.name = text.split(' ', 2)
		self.version = version.strip('E')

@dataclass
class Subgroup:
	name: str
	emojis: List[Emoji]

	def __init__(self, text: str):
		self.name, *emojis = text.split('\n')[:-2]
		emojis = [ Emoji(emoji) for emoji in emojis ]
		self.emojis = [
			emoji for emoji in emojis
			if emoji.status == EmojiStatus.fully
		]

	def __len__(self) -> int:
		return len(self.emojis)

	def count(self) -> int:
		return len(self)

	def string(self) -> str:
		return ''.join(emoji.emoji for emoji in self.emoji)

@dataclass
class Group:
	name: str
	subgroups: Dict[str, Subgroup]

	def __init__(self, text: str):
		self.name, text = text.split('\n\n', 1)
		subgroups, subtotal = text.split(f'# {self.name} subtotal:\t\t', 1)

		subgroups = subgroups.split('# subgroup: ')[1:]
		subgroups = [ Subgroup(subgroup) for subgroup in subgroups ]
		self.subgroups = { subgroup.name: subgroup for subgroup in subgroups }

		subtotal = int(subtotal[:subtotal.index('\n')])
		# filted by status, so subtotal differ
		# assert(self.count() == subtotal)

	def __len__(self) -> int:
		return len(self.subgroups)

	def count(self) -> int:
		return sum(subgroup.count() for subgroup in self.subgroups.values())

	def all_emojis(self) -> List[Emoji]:
		return [ emoji
			for subgroup in self.subgroups.values()
			for emoji in subgroup.emojis
		]

	def string(self) -> str:
		return ''.join(emoji.emoji for emoji in self.all_emojis())


################################################################
#######                      class                       #######
################################################################
class UnicodeEmoji:

	def __init__(self, version: str):
		self.filename: str = f'unicode/emoji-v{version}.ini'
		self.version: str = version
		self.groups: Dict[str, Group] = {}
		self._parse_data()

	def _parse_data(self) -> None:
		with open(self.filename, 'r') as file:
			content = file.read()

		# separate [header, groups, status_counts]
		header, content = content.split('\n\n\n')
		groups, status_counts = content.split('# Status Counts\n')

		# [header] verify version
		version_idx = header.index('Version: ')+9
		version = header[version_idx:header.index('\n', version_idx)]
		assert(self.version == version)

		# [groups] load emojis
		groups = groups.split('# group: ')[1:]
		groups = [ Group(group) for group in groups ]
		self.groups = { group.name: group for group in groups }

		# [status_counts] verify count
		status_counts = status_counts.split('\n')[:-3]
		# filted by status, so subtotal differ

	def count(self) -> int:
		return sum(group.count() for group in self.groups.values())

	def all_emojis(self) -> List[Emoji]:
		return [ emoji
			for group in self.groups.values()
			for emoji in group.all_emojis()
		]

	def string(self) -> str:
		return ''.join(emoji.emoji for emoji in self.all_emojis())

	def print_string(self) -> 'UnicodeEmoji':
		print(self.string())
		return self

	def export_string(self, filename: str=None) -> 'UnicodeEmoji':
		filename = filename if filename else f'string-v{self.version}.txt'

		with open(filename, 'w') as file:
			file.write(self.string())

		return self

	def export_vscode(self, filename: str=None) -> 'UnicodeEmoji':
		filename = filename if filename else f'unicode/vscode-emoji-v{self.version}.txt'
		content = ','.join(f'"{emoji.emoji}":{{"fontCharacter":"{emoji.emoji}","fontSize":"125%"}}' for emoji in self.all_emojis())

		with open(filename, 'w') as file:
			file.write(f'{{{content}}}')

		return self


################################################################
#######                 MAIN STARTS HERE                 #######
################################################################
if __name__ == '__main__':
	(
		UnicodeEmoji(version='12.1')
			.export_vscode()
	)
