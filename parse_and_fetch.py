#
#  Minecraft libraries downloader
#  After downloading replace hostname in version.json with:
#  sed -i 's/libraries\.minecraft\.net/instances.yabko.org\/libraries/g' version.json
#

import json
import os
import shutil
from urllib.parse import urlparse

import requests


def parse_version(filename):
    libraries = []
    with open(filename, 'r') as f:
        version_manifest = json.load(f)

    if version_manifest:
        for library in version_manifest['libraries']:
            libraries.append(library['downloads']['artifact']['url'])

    return libraries


def download_file(url):
    url_parsed = urlparse(url)

    filename = url_parsed.path.strip('/')
    file_path = filename.replace(os.path.basename(filename), '')
    if os.path.exists(filename):
        return
    try:
        os.makedirs(file_path)
    except FileExistsError:
        pass
    with requests.get(url, stream=True) as r:
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


if __name__ == '__main__':
    urls = parse_version('version.json')
    for url in urls:
        download_file(url)
