from datetime import datetime
import urllib.request
import os

# Checks for log file
print("Checking for log file")

if (os.path.isfile('cache.log') == False):
    print('Log file not downloaded, downloading now...')
    url = 'https://s3.amazonaws.com/tcmg476/http_access_log'
    urllib.request.urlretrieve(url, 'cache.log')
    print('Log downloaded!')
else:
    print('Cache log is already downloaded')

# Open File
file = open("cache.log", "r", encoding="windows-1252")
print('Beginning log inspection...')

# Analysis
for line in file:
    lines = line.split(" ")
    if len(lines) < 10:
        continue

file.close()

# Output Info