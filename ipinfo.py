#!/usr/bin/env python3

import re
import socket
import requests
import sys
from tldextract import extract
import validators

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
    
    # match = re.search(DOMAIN_REGX, argv.lower())
    # ip_info = []
    # if match:
    #     ip = socket.gethostbyname(argv)
    #     ip_info = request_to_ipinfo(ip)
    # else:
    #     ip_info = request_to_ipinfo(argv)

    all_keys = [
        'ip', 'hostname', 'city', 'region', 'country',
        'org', 'postal', 'loc'
    ]
    print('host: ' + argv.lower())
    for k in all_keys:
        try:
            print(u'{}'.format(ip_info[k]))
        except KeyError:
            pass


if __name__ == "__main__":
    
    ARG1 = sys.argv[1]
    
    if len(sys.argv) == 1:
        print(request_to_ipinfo("")["ip"])
        sys.exit(0)

    if validators.ipv4(ARG1):
        main(ARG1)
        sys.exit(0)

    if validators.url(ARG1) or validators.domain(ARG1):
        tsd, td, ts = extract(ARG1)
        host = td + '.' + ts
    host = ARG1
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        print("Host is invalid or not resolvable.")
        sys.exit(1)
    main(host)
