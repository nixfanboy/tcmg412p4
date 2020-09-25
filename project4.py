from datetime import datetime
import urllib.request
import os
from collections import Counter

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
print('Beginning log inspection...')

# Collect Info
days = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0} # 0 = Monday, 1 = Tuesday, 2 = Wednesday, etc
weeks = {}
months = {}
files = {}
errors = 0
redirects = 0
total_requests = 0

#Opening File
file = open("cache.log", "r", encoding="windows-1252")

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


#Indexing Data
file_count = Counter(files)
months_count = Counter(months)
weeks_count = Counter(weeks)
days_count = Counter(days)

top_file = file_count.most_common(1) #most common file
bottom_file = file_count.most_common()[-1] #least common file

# Selecting Data to Show.
print("\nLog Analysis Complete! What would you like to see?")

# Set an initial value for choice other than the value for 'quit'.
choice = ''
choice2 = ''
# Start a loop that runs until the user enters the value for 'quit'.
while choice != 'q':
    # Give all the choices in a series of print statements.
  print("\n[1] Enter 1 to Enter Request Analysis by Date.")
  print("[2] Enter 2 to See Most/Least Requested File.")
  print("[3] Enter 3 to Unsuccesful/Redirect Request Percentage")
  print("[q] Enter q to quit.")
    
    # Ask for the user's choice.
  choice = input("\nWhat would you like to see? ")
    
    # Respond to the user's choice.
  if choice == '1': 

        while choice2 != 'q':
        # Requests by Date menu
          print("\n[1] Enter 1 for Requests by Date")
          print("[2] Enter 2 for Requests per week.")
          print("[3] Enter 3 for Requests per month")
          print("[q] Enter q to go back.")

          choice2 = input("\nWhat would you like to see?")

          if choice2 == '1':
            print("\nRequests per day: ", list(days_count.items()),"\n")
        
          elif choice2 == '2':
            print("Requests per Week: ", list(weeks_count.items()),"\n")
        
          elif choice2 == '3':
            print("Requests per Month: ", list(months_count.items()),"\n")
        
          elif choice2 == 'q':
            print("\n")

  elif choice == '2':
    print("\nMost accessed file: ",top_file,"\n" )
    print("\nLeast accessed file: ",bottom_file,"\n" )

  elif choice == '3':
    print("\nPercentage of Requests as Errors: ",round((errors*100)/total_requests,2),"%\n")

    print("\nPercentage of Requests as Redirects: ", round((redirects*100)/total_requests,2),"%\n")

  elif choice == 'q':
      print("\nUntil next time.\n")
  else:
      print("\nI don't understand that choice, please try again.\n")
