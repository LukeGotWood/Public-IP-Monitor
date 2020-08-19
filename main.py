# main.py

# Import all used modules
import http.client, urllib, urllib.request
import os
from dotenv import load_dotenv
import re

# Check for .env
if not os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.env')):
    print('No .env file found...\nExiting...')
    sys.exit(1)

# Load enviromental variables
load_dotenv()
TOKENKEY = os.getenv('TOKENKEY')
USERKEY = os.getenv('USERKEY')

# Declare variables
old_ip = 'NA.NA.NA.NA'
ip = ''

# Declare functions
def pushNotification(msg):
    conn = http.client.HTTPSConnection('api.pushover.net:443')
    conn.request('POST', '/1/messages.json',
    urllib.parse.urlencode({
        'token': TOKENKEY,
        'user': USERKEY,
        'message': msg,
    }), { 'Content-type': 'application/x-www-form-urlencoded' })
    conn.getresponse()

# -------- Main Body --------

# Check if ip file exists and retrieve ip
if os.path.isfile('ip.txt'):
    print('File exist')
    with open('ip.txt', 'r') as f:
        old_ip = f.read()
else:
    print('File not exist')

# Validate ip address
if re.match(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', old_ip):
    print('Ip Valid')
else:
    print('Ip Invalid')
    old_ip = 'NA.NA.NA.NA'

# Check current ip
page = urllib.request.urlopen('http://checkip.dyndns.org/').read().decode()
new_ip = re.search(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', page).group(0)
print(f'New ip \'{new_ip}\'')

if old_ip != new_ip:
    print(f'Current ip \'{old_ip}\' does not match new ip \'{new_ip}\'')
    pushNotification(f'Ip Address has changed from \'{old_ip}\' to \'{new_ip}\'')
    with open('ip.txt', 'w') as f:
        f.write(new_ip)
else:
    print(f'Current ip \'{old_ip}\' matched new ip \'{new_ip}\'')

# -------- END Main Body --------