# Tools for build
import PyInstaller.__main__
import shutil
import os

# Make new languages.zip
if os.path.exists(os.getcwd() + '/languages/languages.zip'):
    os.remove(os.getcwd() + '/languages/languages.zip')
shutil.make_archive("languages", 'zip', os.getcwd() + '/languages/')

# Removing dist
if os.path.exists(os.getcwd() + '/dist'):
    shutil.rmtree(os.getcwd() + '/dist')

# Build app
PyInstaller.__main__.run([
    'main.spec'
])
