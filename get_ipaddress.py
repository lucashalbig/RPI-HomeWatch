#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import check_output
import re
import sys

def printX(text, end = '\n'):
    version = sys.version
    just_version = int(version.split('(')[0].replace('.','')[:2])
    #~ print(just_version)
    if just_version < 35:
        from printhelper import printPythonPre36
        printPythonPre36(text, end)
    else:
        from printhelper2 import printPython36
        printPython36(text, end)

def getIPs():
	lines = check_output(['ifconfig'])
	if type(lines) == bytes:
		lines = lines.decode()
		
	lines = lines.split('\n')
	ips = []
	for line in lines:
		if line.strip().startswith('inet'):
			x = re.search('inet ([^ ]+) .+', line.strip())
			if x:
				ip = x.group(1)
				if ip != '127.0.0.1':
					ips.append(ip)
	return ips

if __name__ == '__main__':
    ips = getIPs()
    if len(ips) > 0:
        if len(ips) > 1:
            printX('Sie können eine der folgenden IPs verwenden:')
        else:
            printX('Dies ist ihre IP:')
        for IP in ips:
            printX(IP)