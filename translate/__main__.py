'''	Copyright © 2022 mightbesimon.com
	All rights reserved.

	Material belonging to others may have been
	used under Creative Commons Licence or with
	explicit or implicit permission.
'''

from .file_icons import FileIconMapper

################################################################
#######                 MAIN STARTS HERE                 #######
################################################################
(
	FileIconMapper(filename='references/file-icons.md')
		.export_icon_theme()
		.update_readme()
)
