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
days = {"Sunday": 0, "Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0}
weeks = {}
months = {}
files = {}
errors = 0
redirects = 0
for line in file:
    lines = line.split(" ")
    if len(lines) < 10:
        continue
    date = date = datetime.strptime(lines[3], "[%d/%b/%Y:%H:%M:%S")
    filename = lines[6]
    response = lines[8]

file.close()

# Output Info