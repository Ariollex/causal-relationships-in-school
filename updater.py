from tqdm import tqdm
from sys import exit
import subprocess
import requests
import platform
import debug
import json
import os

# supported systems
supported_os = 'Windows'

# variables
is_debug = False


def set_variables(is_debug_main):
    global is_debug
    is_debug = is_debug_main


def is_updater_supported():
    if platform.system() not in supported_os:
        return -1


def get_int(text):
    return int(''.join([s for s in text if s.isdigit()]))


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
    update_updater()
    file_name = generate_file_name(latest_version)
    # Start Updater
    start_updater(latest_version, file_name)


def start_updater(latest_version, file_name):
    url = 'https://github.com/Ariollex/causal-relationships-in-school/releases/download/' \
         + latest_version + '/' + file_name + '.zip'
    args = ['./Updater.exe',
            '--url=' + url,
            '--archive_name=' + file_name,
            ]
    if is_debug:
        print(debug.i(), 'Starting Updater...')
    subprocess.Popen(args)
    exit()


def get_version_updater():
    if not os.path.exists(os.getcwd() + '/Updater.exe'):
        return -1
    result = subprocess.run(['./Updater.exe', '--version'], capture_output=True)
    return result.stdout.decode("utf-8").strip()


def update_updater():
    url = 'https://api.github.com/repos/ariollex/Updater/releases/latest'
    latest_response = requests.get(url)
    if is_debug:
        print(debug.i(), 'Checking updates for Updater...')
    if latest_response.status_code == 200:
        if is_debug:
            print(debug.i(), 'Server response received...')
        response_data = json.loads(latest_response.text or latest_response.content)
        latest_version = response_data['tag_name']
        if is_debug:
            print(debug.i(), 'Latest Updater version on server:', latest_version)
        if get_int(latest_version) > get_int(get_version_updater()) or get_version_updater == -1:
            if os.path.exists('Updater.exe'):
                if is_debug:
                    print(debug.i(), 'Update available for Updater!')
                os.remove('Updater.exe')
            else:
                if is_debug:
                    print(debug.i(), 'Updater not found! Downloading latest version')
            url = 'https://github.com/Ariollex/Updater/releases/download/' + latest_version + '/Updater.exe'
            response = requests.get(url, timeout=None)
            with open('Updater.exe', "wb") as file:
                file.write(response.content)
            return 0
        else:
            if is_debug:
                print(debug.i(), 'The latest update of Updater is already installed!')
            return 0
    else:
        return -1
