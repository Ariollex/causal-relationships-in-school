# Tools for build

import shutil
import os

# Make languages.zip


def make_archive(source, destination):
    base = os.path.basename(destination)
    name = base.split('.')[0]
    f_format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, f_format, archive_from, archive_to)
    shutil.move('%s.%s' % (name, f_format), destination)


if os.path.exists('languages/languages.zip'):
    os.remove('languages/languages.zip')

make_archive('languages/', 'languages/languages.zip')
