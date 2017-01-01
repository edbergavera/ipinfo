#!/usr/bin/env python3

import re
import socket
import requests
import sys

DOMAIN_REGX = r'([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}'

IPINFO_URL = 'http://ipinfo.io/'


def request_to_ipinfo(ip):
    ''' returns JSON from the request '''
    full_url = 'http://ipinfo.io/{}'.format(ip)
    headers = {'User-Agent': 'curl/7.43.0'}
    req = requests.get(full_url, headers=headers)
    if req.status_code == 200:
        return req.json()

def main(argv):

	match = re.search(DOMAIN_REGX, argv.lower())
	ip_info = []
	if match:
		ip = socket.gethostbyname(argv)
		ip_info = request_to_ipinfo(ip)
	else:
		ip_info = request_to_ipinfo(argv)

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
	try:
		socket.gethostbyname(sys.argv[1])
	except socket.gaierror:
		print("Host is invalid or not resolvable.")
		sys.exit(1)
	main(sys.argv[1])
