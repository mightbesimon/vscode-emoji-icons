'''	Copyright © 2022 mightbesimon.com
	All rights reserved.

	Material belonging to others may have been
	used under Creative Commons Licence or with
	explicit or implicit permission.
'''

from .file_icons import FileIconMapper
from .product_icons import ProductIconMapper

################################################################
#######                 MAIN STARTS HERE                 #######
################################################################
(
	FileIconMapper(filename='references/file-icons.md')
		.export_icon_theme(filename='file-icons/emoji-icon-theme.json')
		.update_readme()
)
(
	ProductIconMapper()
		.load_reference(filename='references/product-icons.md')
		.export_icon_theme(filename='product-icons/emoji-product-icon-theme.json')
		.update_readme()
)
(
	ProductIconMapper()
		.load_reference(filename='references/product-icons.md')
		.load_reference(filename='references/product-icons-fun.md')
		.export_icon_theme(filename='product-icons/emoji-fun-product-icon-theme.json')
		.update_readme()
)
