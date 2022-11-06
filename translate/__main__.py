'''	Copyright © 2022 mightbesimon.com
	All rights reserved.

	Material belonging to others may have been
	used under Creative Commons Licence or with
	explicit or implicit permission.
'''

from .models import IconType
from .file_icons import FileIconMapper
from .product_icons import ProductIconMapper

################################################################
#######                 MAIN STARTS HERE                 #######
################################################################
(
	FileIconMapper()
		.load_reference(filename='references/file-icons.md', icon_type=IconType.file)
		.load_reference(filename='references/extension-icons.md', icon_type=IconType.extension)
		.load_reference(filename='references/folder-icons.md', icon_type=IconType.folder)
		.export_icon_theme(filename='file-icons/emoji-icon-theme.json')
		.update_readme()
)
(
	ProductIconMapper()
		.load_reference(filename='references/product-icons.md', icon_type=IconType.product)
		.export_icon_theme(filename='product-icons/emoji-product-icon-theme.json')
		.update_readme()
)
(
	ProductIconMapper()
		.load_reference(filename='references/product-icons.md', icon_type=IconType.product)
		.load_reference(filename='references/product-icons-fun.md', icon_type=IconType.product)
		.export_icon_theme(filename='product-icons/emoji-fun-product-icon-theme.json')
		.update_readme()
)
