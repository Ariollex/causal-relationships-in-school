from tkinter import messagebox
import subprocess
import requests
import platform
import debug
import json
import sys
import os

# supported systems
supported_os = ('Windows', 'Darwin')

# variables
is_debug = False
base_path = os.getcwd()

# Updater app
if platform.system() == 'Darwin':
    updater_name = 'Updater.app'
else:
    updater_name = 'Updater.exe'


def set_variables(is_debug_main, base_path_main):
    global is_debug, base_path
    is_debug = is_debug_main
    base_path = base_path_main


def generate_file_name(latest_version):
    file_name = str(latest_version)
    if platform.system() == 'Windows':
        file_name = file_name + '-Windows'
    else:
        file_name = file_name + '-macOS'
    return file_name


def start_update(latest_version):
    if is_debug:
        print(debug.i(), 'Starting update...')
    file_name = generate_file_name(latest_version)
    # Start Updater
    start_updater(latest_version, file_name)


def start_updater(latest_version, file_name):
    url = 'https://github.com/Ariollex/causal-relationships-in-school/releases/download/' \
          + latest_version + '/' + file_name + '.zip'
    if platform.system() == 'Darwin':
        args = ['open', base_path + '/' + updater_name, '--args',
                '--url=' + url,
                '--archive_name=' + file_name,
                ]
    else:
        args = ['./' + updater_name,
                '--url ' + url,
                '--archive_name ' + file_name,
                ]
    if is_debug:
        print(debug.i(), 'Starting Updater...')
    subprocess.Popen(args)
    sys.exit()
