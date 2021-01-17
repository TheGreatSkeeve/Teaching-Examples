'''
Importing Modules to Use in Your Script

Like most languages, Python is rich in libraries that you can import into your code to add functionality
Some libraries come with Python by default, and are automatically imported, like print, len, etc..
Some libraries come with Python by default, but you have to manually import them.  For example, time.sleep

time is a large library, we don't need everything in there.  We just need one function.  In that case, you can execute
"from libraryname import functionname"

if you want to import the full library, just do "import libraryname"
'''

from time import sleep      # Import the sleep function from the time library
import time                 # Import the whole time library

# Now that we have imported sleep from time, we can use it to pause our script if we want.
sleep(10)   # This will pause the script for ten seconds.


'''''''''
Some common libraries...or, at least some libraries I find myself using frequently.
'''''''''

'''
os

Allows you to interact with the underlying operating system
It's essentially like a command prompt.
'''
import os
os.system("ipconfig /renew")    # This will send a commend to the system to renew the IP configuration of the local machine

filepath = "C:/users/steve/desktop/test.txt"    # Set a test file path
os.path.exists(filepath)                        # If the file exists, returns true.  If not, returns false.
os.remove(filepath)                             # Deletes file

path = "C:/users/steve/desktop/test_folder/"    # Set a test folder path
os.path.isdir(path)                             # This will return True if the above directory exists, False if not
os.rmdir(path)                                  # Deletes the folder

os.chdir(path)                                  # Change directories

file="setup.exe"
os.startfile(file)                           # Start a file
'''
subprocess

Allows you to spawn new processes, connect to input / output / error, and return codes
More versatile than os, but has quirks
'''

# This is a simple function using subprocess to run a command with powershell
# Takes in "filename" which can be anything from a command (ls, Write-Host "Hello", etc) to an actual file to execute
# Returns feedback from command, needs to be parsed because Powershell comes out ugly as hell
import subprocess
def powershellRun(filename):
    process = subprocess.Popen('powershell.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(filename.encode('utf-8'))
    return out

response = powershellRun(".\\script.ps1")


'''
random

Easy generation of random numbers for things.
'''

import random
num = random.randint(0,1000)    # Get a random number between 0 and 1000


# Get a little more complex...
def randomTest(rangenum):
    counter = [0] * rangenum                # Create a list to count how many times each number gets called by Random
    for i in range(0,rangenum):             # Cycle through as many times as rangenum says
        num = random.randint(0,rangenum)    # Generates the random number
        counter[num] += 1                   # Adds one to the "counter" entry, using the random number as the slot number.  So, if it calls number 165, this will add +1 to the value of counter[165], showing that it came up
        print("NUMBER: " + str(num))        # Prints the number that came up
        print("NUMBER'S SCORE: " + str(counter[num]) + "\n" )   # Prints how many times that number came up
    return counter                          # Returns counter, which is the score list

# Call the function and set results to a variable
numberlist = randomTest(1000)


'''
winsound
'''

# Library to make the computer beep
# I don't really have a reason for including this, it's just fun.

import winsound

def beep_beep_motherfucker(frequency,duration,repeat):
    for i in range(0, repeat):
        winsound.Beep(frequency, duration)

beep_beep_motherfucker(1000,100,5)


'''
datetime
'''

# The easiest way to get time / date information is with DateTime.
from datetime import datetime
now = datetime.now()
now.strftime("%m-%d-%Y")        # Month-Day-Year
now.strftime("%H:%M:%S")        # Hour-Minute-Second


'''
Requests
'''

# Sent and recieve data over the network
import requests

url = "http://canhazip.com"     # This is a website that tells you what your public IP address is.  Easy example.
data = requests.get(url)   # Use requests.get(url) to grab the response data
print(data.text)            # Prints the text value of the website, this should be all the HTML on the page
print(data.content)         # Prints the page's HTML, but in binary
print(data.url)             # In case you forgot what the URL was

data = data.text            # This sets data to the text value of the web page
data = data.split("\n")     # In this instance, the data is only going to be the IP address.  However, we do have a rude trailing "\n" to get rid of.
data = data[0]              # Remember, if you use .split to completely truncate a string, the result will be a two-entry list.  Gotta grab the first entry.

# This can also be condensed, if you want.
# Note, this is relevant to pretty much all commands, not just this.
data = requests.get(url)
data = data.text.split("\n")[0]

# You can go a little bit further, even.
data = requests.get(url).text.split("\n")[0]


'''
praw

Alright, here's a more interesting example.  Praw is Reddit's own library for Python for interacting with Reddit.
Praw is external to Python, so you'll have to install it.  Go to the command line (cmd or powershell) and run:
pip install praw

Now, you can go back to Python and import praw.
'''
import praw     # Import all libraries from praw

'''
Create a "reddit" object, using praw.Reddit.
This is essentially a shortcut.  Python libraries go on and on sometimes, this cleans things up.  
'''
reddit = praw.Reddit(client_id='xbybwyprJPjV7w',
                     client_secret='PtFipot76-YFNcpTPbsNkWTuJPM64g',
                     user_agent='Anti Rick Roll Bot',
                     username='TheGreatSkeeve_',
                     password='Seraph@INK45)')

# Uses the above object to create a subreddit object
# Since this includes the "reddit" object, it will include the authentication / user config provided.
subreddit = reddit.subreddit('all')

# This function accesses a subreddit's Comment Stream.
# It reads the most recent 100 comments (Or whatever you set the limit to) and then waits
# for new comments.
def readComments(subreddit):
    for comment in subreddit.stream.comments():
        if comment.author.name == 'TheGreatSkeeve':    #   Check if I am the author
            print("Found a comment of ours!")