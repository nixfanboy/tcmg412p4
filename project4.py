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

# Collect Info
days = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0} # 0 = Monday, 1 = Tuesday, 2 = Wednesday, etc
weeks = {}
months = {}
files = {}
errors = 0
redirects = 0
total_requests = 0
for line in file:
    lines = line.split(" ")
    if len(lines) < 10:
        continue
    total_requests += 1
    date = datetime.strptime(lines[3], "[%d/%b/%Y:%H:%M:%S")
    filename = lines[6]
    response = lines[8]

    days[date.weekday()] += 1

    week_str = str(date.isocalendar()[1]) + " " + str(date.year) # e.g. week 44 of 1994 = "44 1994"
    if week_str in weeks:
        weeks[week_str] += 1
    else:
        weeks[week_str] = 1

    month_str = str(date.month) + " " + str(date.year) # e.g. Nov 1994 = "11 1994"
    if month_str in months:
        months[month_str] += 1
    else:
        months[month_str] = 1

    if filename in files:
        files[filename] += 1
    else:
        files[filename] = 1

    if response[0] == "4":
        errors += 1
    elif response[0] == "3":
        redirects += 1

file.close()

# Analyze Info
file_count = Counter(files)
top_file = file_count.most_common(1) #most common file
bottom_file = file_count.most_common()[-1] #least common file

print("log inspection completed")
print("Most accessed file: ",top_file )
print("least accessed file: ",bottom_file )


print("Total Number of Requests: ", total_requests)
print("Percentage of Requests as Errors: ",round((errors*100)/total_requests,2),"%")
print("Percentage of Requests as Redirects: ", round((redirects*100)/total_requests,2),"%")



# Output Info
