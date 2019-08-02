#!/usr/bin/env python3

import re
import socket
import requests
import sys
from tldextract import extract

DOMAIN_REGX = r'([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}'

IPINFO_URL = 'https://ipinfo.io/'


def request_to_ipinfo(ip):
    """ returns JSON from the request """

    full_url = 'http://ipinfo.io/{}'.format(ip)
    headers = {'User-Agent': 'curl/7.65.3'}
    req = requests.get(full_url, headers=headers)
    if req.status_code == 200:
        return req.json()


def main(argv):
    ip = socket.gethostbyname(argv.lower())
    ip_info = request_to_ipinfo(ip)

    all_keys = [
        'ip', 'hostname', 'city', 'region', 'country',
        'org', 'postal', 'loc'
    ]

    for k in all_keys:
        try:
            print(u'{}'.format(ip_info[k]))
        except KeyError:
            pass


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(request_to_ipinfo("")["ip"])
        sys.exit(0)
    tsd, td, ts = extract(sys.argv[1])
    dom = td + '.' + ts
    try:
        socket.gethostbyname(dom)
    except socket.gaierror:
        print("Host is invalid or not resolvable.")
        sys.exit(1)
    main(dom)
