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
	folder_name    = 'folderNames'

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
		self.names = names.split(' | ')
		self.comment = comment[0].rstrip(')') if comment else None

		if icon_type == IconType.file_extension:
			self.names = [ name.lstrip('.') for name in self.names ]

@dataclass
class IconItem:
	icon_type: IconType
	name: str
	emoji: str
