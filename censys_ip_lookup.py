#!/usr/bin/python

# Censys IP lookup script - Need work

import argparse
import sys
import json
import requests
import time

censys_id = ""
censys_secret = ""

censys_id_2 = ""
censys_secret_2 = ""

main_url = "https://www.censys.io/api/v1"

def censys_lookup(ips, out):
	count = 0
	for ip in ips:
		if count >= 10:
			count = 0
		if count != 5:
			res = requests.get(main_url + "/view/ipv4/"+ip, auth=(censys_id_2, censys_secret_2))
			count = count + 1
		elif count >= 5 and count != 10:
			res = requests.get(main_url + "/view/ipv4/"+ip, auth=(censys_id, censys_secret))
			count = count + 1
		jso = res.json()
		time.sleep(2)
		try:
			ip_from_json = jso["ip"]
			ports_from_json = jso["protocols"]
			for x in jso["protocols"]:
				with open(out, "a") as output:
					print ip_from_json + ": " + str(x)
					output.write(ip_from_json + ": " + str(x))
					output.write("\n")
					output.close
		except:
			print "ip - " + ip + " Not Found"

def main():
	usage = """Censys Lookup"""
	parser = argparse.ArgumentParser(usage=usage)
	parser.add_argument('-f', help='The file containing a list of IPv4 addresses', dest='ip_file', action='store', required=True)
	parser.add_argument('-o', help='Output file for the list of IPs and the associated ports', dest='out_file', action='store', required=True)
	opts = parser.parse_args()
	out = opts.out_file
	ips = [line.rstrip('\n') for line in open(opts.ip_file)]
	censys_lookup(ips, out)

if __name__ == "__main__":
	main()
