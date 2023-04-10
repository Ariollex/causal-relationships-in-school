# Tools for build
import PyInstaller.__main__
import pyinstaller_versionfile
from version import version
import platform
import shutil
import os

# Make new languages.zip
if os.path.exists(os.getcwd() + '/languages/languages.zip'):
    os.remove(os.getcwd() + '/languages/languages.zip')
shutil.make_archive("languages", 'zip', os.getcwd() + '/languages/')

# Removing dist
if os.path.exists(os.getcwd() + '/dist'):
    shutil.rmtree(os.getcwd() + '/dist')

# Variables
app_name = "Updater"
app_description = "Causal_relationships_in_school"

if platform.system() == 'Windows':
    # Make version file for exe
    pyinstaller_versionfile.create_versionfile(
        output_file="version_file.txt",
        version=version + '.0',
        file_description=app_description,
        internal_name=app_name,
        original_filename=app_name + ".exe",
        product_name=app_name,
        translations=[1033, 1252, 1251]
    )

# Build application
PyInstaller.__main__.run([
    'main.spec'
])
