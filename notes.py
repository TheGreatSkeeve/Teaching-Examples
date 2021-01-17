import os
import sys

import logging
import time
import zmq
import json
from datetime import datetime
import sqlite3
from pathlib import Path

import glob
import ntpath
import subprocess
import winreg
from pathlib import Path

import PySimpleGUI as sg
import wincertstore
import subprocess
import pyAesCrypt
import os

if not ".rdp" in content:
    print("RDP is not in " + content)
else:
    print("This is an RDP file")
    x = content.split(".rdp")
    print(x[0])
    xx = parseRDP(x[0])
try:
    print(xx + "\n")
    sqlite_write_rdp(xx[0], xx[1], xx[2])
except:
    print("Writing to SQL failed")


# Super simple function to run something with Powershell
# Takes in "filename" which can be anything from a command (ls, Write-Host "Hello", etc) to an actual file to execute
# Returns feedback from command, needs to be parsed because Powershell comes out ugly as hell
def powershellRun(filename):
    process = subprocess.Popen('powershell.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(filename.encode('utf-8'))
    return out


# Encrypt a provided password using Powershell's SecureString function
# The three single-quotes allow a variable to span multiple lines, thereby submitting multiple commands to Powershell
def encryptPassword(password):
    command = '''$x = (convertto-securestring -string "%s" -asplaintext -force | convertfrom-securestring)
    write-host $x'''
    command = command % password  # "%" puts the password into command, wherever the %s is.
    out = powershellRun(command)
    output = (([x.decode("utf8") for x in out.split(b"write-host $x")])[1].split("\n"))[0]  # There's the parsing.
    secureString = output
    return secureString


# Decrypt a secure string using Powershell
def decryptPassword(securePassword):
    command = '''
    $secureObject = ConvertTo-SecureString -String %s
    $decrypted = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureObject)
    $decrypted = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($decrypted)
    write-host $decrypted
    '''
    command = command % securePassword
    out = powershellRun(command)
    output = (([x.decode("utf8") for x in out.split(b"$decrypted\n")])[1].split("\n"))[0]
    return output


# How to read / write / append to a text file (Or any file)
# I always forget how to do this.
# Give the function the filename (Or full file path), the mode ([r]ead, [w]rite, [a]ppend, and the content (If you're writing to the file)
def editFile(filename, mode, content=None, multiline=None):
    if mode == "r":
        with open(filename, mode) as file:
            data = file.read()
            file.close()
    elif multiline == True:  # Can write multi-line / arrays as well
        for i in range(0, len(content)):
            with open(filename, mode) as file:
                file.write(content[i] + "\n")
                file.close()
    else:
        with open(filename, mode) as file:
            file.write(content)
            file.close()


def readFile(filename):
    filename = "conf/" + filename + ".conf"  # Set the path
    count = len(open(filename).readlines())  # Find out how many lines there are in the config doc
    entries = [None] * count  # Make an any array with enough slots for each line
    i = 0
    with open(filename, "r") as f:  # Open the config file
        for line in f.readlines():  # Read through and assign each line to a slot for entries
            entries[i] = line
            i += 1
    return entries


def readCreds(filename):
    entries = readFile(filename)
    wmi = []
    ans = []
    username = ""
    password = ""
    for x in range(0, len(entries)):
        if "fu=" in entries[x]:
            username = decryptPassword(((entries[x]).strip("fu=")))
        if "fp=" in entries[x]:
            password = decryptPassword(((entries[x]).strip("fp=")))
        if "wmi=" in entries[x]:
            val = (entries[x].strip("wmi=")).strip("\n")
            wmi.append(decryptPassword(str(val)))
        if "ans=" in entries[x]:
            val = (entries[x].strip("ans=")).strip("\n")
            ans.append(decryptPassword(str(val)))
        if "u:" in entries[x]:
            print("This will return any Username")
            print("Title comes after the colon, parse that out")
            print("Titles should be unique")
            print("Can also pull u: to get the titles of the credentials for a dropdown")
        if "p:" in entries[x]:
            print("Same, but for passwords.  Title and everything.")

    final = (username, password, wmi, ans)
    return final


def lock(filename, password):
    oldpath = "conf/" + filename + ".conf"
    newpath = "conf/" + filename + ".locked"
    # encryption/decryption buffer size - 64K
    bufferSize = 64 * 1024
    pyAesCrypt.encryptFile(oldpath, newpath, password, bufferSize)
    os.remove(oldpath)


def unlock(filename, password):
    oldpath = "conf/" + filename + ".locked"
    newpath = "conf/" + filename + ".conf"
    bufferSize = 64 * 1024
    pyAesCrypt.decryptFile(oldpath, newpath, password, bufferSize)
    os.remove(oldpath)


dbfolder = "db/"
dbname = "tyler.db"
confirmation = "Message received by Primary Node"
Path(dbfolder).mkdir(parents=True, exist_ok=True)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:50165")
import re


# Encoding stuff
# List item separator       ;
# List List separator       \n
def encodeData(data):
    return str.encode(data)


def encodeList(LIST):
    toReturn = ""
    separator = ">;"
    for i in range(0, len(LIST)):
        toReturn = toReturn + str(LIST[i]) + separator
    return encodeData(toReturn)


def decodeData(data):
    return (data.decode())


def decodeList(encoded_string):
    separator = ">;"
    returned = decodeData(encoded_string)
    List = returned.split(separator)
    return list(filter(None, List))


def socketListener(msg):
    for i in range(0, 5):
        print("\n\nListening...")
        # msg_bytes = str.encode(msg)
        message = socket.recv()  # Wait for next request from client
        decoded = decodeList(message)
        for val in decoded:
            print(val)
        # sqlite_write(datetime.now(),decoded[0],decoded[1])
        socket.send(encodeData(confirmation))  # Send reply back to client


while True:
    socketListener(confirmation)

# Configure log file
logging.basicConfig(
    filename='InfraVision.log',
    level=logging.DEBUG,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)

# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)

os.path.isdir(path)
# True or false if path variable is a directory

os.rmdir(path)
# Removes path

# THese throw OSError:

os.path.exists(path)
# If file exists

os.remove(path)
# Delete file


newCert = "New-SelfSignedCertificate -subject \"CN=Steve's RDP Manager\" -CertStoreLocation Cert:\CurrentUser\My -FriendlyName \"Steve's RDP Manager\" -NotAfter (Get-Date).AddYears(10)"

getThumb = '''
$x = Get-ChildItem  -Path Cert:\CurrentUser\My | Where-Object {$_.Subject -Match \"Steve's\"} | Select-Object Thumbprint
$x = $x.thumbprint
$x
'''


def set_reg(name, value):
    REG_PATH = r"SOFTWARE\Microsoft\Terminal Server Client\PublisherBypassList"
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                      winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_DWORD, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


# Get a list of the RDP Files in the Connections folder
def getFiles():
    filelist = glob.glob("connections/" + '*.rdp')
    namesonly = []
    for file in filelist:
        name = (ntpath.basename(file)).split(".", 1)
        namesonly.append(name[0])
    return namesonly


currentlist = getFiles()


# Manually connect to a server via IP and port
def connectRDP_Manual(IP, port):
    connection = exe + " /v:" + str(IP) + ":" + str(port)
    powershellRun(connection)


# Run a Powershell command / open a file with Powershell
def powershellRun(filename):
    process = subprocess.Popen('powershell.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(filename.encode('utf-8'))
    return out


# Write an RDP file
def createRDP(filename, contents, sign):
    try:
        with open(filename, "w") as f:
            f.write(contents)
            f.close()
    except Exception as e:
        print(e)
    if sign == "sign":
        thumb = certCheck()
        command = "rdpsign /sha256 " + thumb + " " + filename
        powershellRun(command)


# Creates a new cert
# Called if certCheck cannot find the cert in the personal store
# Returns thumbprint of cert
def certSetup():
    try:
        powershellRun(newCert)
        out = powershellRun(getThumb)
        out = [x.decode("utf8") for x in out.split(b"$x\n") if len(x) > 35]
        last = out[1].split("\r", 1)
        thumbprint = last[0]
    except:
        print("Something went wrong with generating the cert")
    try:
        set_reg(thumbprint + "00", 0x0000004c)
    except:
        print("Something went wrong trusting the cert")
    return thumbprint


# Find if the "Steve's RDP Manager" cert is in the provided store
def certCount(storename):
    store = wincertstore.CertSystemStore(storename)
    count = 0
    for cert in store.itercerts():
        if "Steve's RDP Manager" in cert.get_name():
            count += 1
    return count


# Returns personal cert thumbprint, generates cert if necessery
def certCheck():
    count = certCount("MY")
    if count > 0:
        out = powershellRun(getThumb)
        out = [x.decode("utf8") for x in out.split(b"$x\n") if len(x) > 35]
        last = out[1].split("\r", 1)
        thumbprint = last[0]
    if count == 0:
        thumbprint = certSetup()
    root_add()
    return thumbprint


def root_add():
    count = certCount("ROOT")
    if count == 0:
        window2 = sg.Window("Alert", [
            [sg.Text(
                "We're going to install the application's cert in your Trusted Root Certificate Authorities, please approve the next prompt.")],
            [sg.OK()]
        ])
        window2.read()
        window2.close()
        powershellRun("./addroot.ps1")


def parseRDP(rdpfile):
    returned = [None] * 5
    if "connections" in rdpfile:
        filename = rdpfile + ".rdp"
    else:
        filename = "connections/" + rdpfile + ".rdp"
    openme = open(filename, "r")
    for i in range(0, 5):
        line = openme.readline()
        if "full address" in line:
            line = line.split(":")
            x = line[2].split("\n")
            returned[0] = (x[0])
        if "username" in line:
            line = line.split(":")
            x = line[2].split("\n")
            returned[1] = (x[0])
        if "password" in line:
            line = line.split(":")
            x = line[2].split("\n")
            returned[2] = (x[0])
    return returned


# Get a list of the RDP Files in the Connections folder
def getFiles():
    # Glob apparently pulls directory contents...?
    filelist = glob.glob("connections/" + '*.rdp')
    # Initialize empty array
    namesonly = []
    for file in filelist:
        # Pull the file name
        name = (ntpath.basename(file)).split(".", 1)
        # Lose the extension and write to namesonly
        namesonly.append(name[0])
    return namesonly


# Write an RDP file
def createRDP(filename, contents):
    # Open the filename the user provided
    with open(filename, "w") as f:
        # Write the user provided content to it
        f.write(contents)
        f.close()


# Print buckets to make sure we're connected
for bucket in s3.buckets.all():
    print(bucket.name)

# Keys:
#   Keys must not start with a slash
#   Keys must end in a slash if creating a folder
#   Creating a subfolder or file also creates parent folders if they don't exist


##########
##########  Running multiple commands in the same shell session, fuck this is handy
##########

commands = '''
enter commands here
One per line
No quotes required
'''

process = subprocess.Popen('powershell.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, err = process.communicate(commands.encode('utf-8')
print
out

import random

sub = porno[random.randint(0, 472)]

# This makes the config folder if it doesn't exist_ok
# Config folder is where the database goes
Path(dbfolder).mkdir(parents=True, exist_ok=True)

# Initialize the database
rss_dict = {}

days = [x for x in range(1, 11)]

Sets
days
to[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Don
't fucking know why.
Don
't fucking know why.


def beepbeepmotherfucker():
    import winsound
    frequency = 1000
    duration = 100
    for i in range(0, 5):
        winsound.Beep(frequency, duration)

        if (len(a) > 1):
            a = a.split("\n")

            # https://api.telegram.org/bot1387703254:AAGmqzewKexbjYUgTxhpu-w-9EZvOsZweTQ/sendMessage?chat_id=-1001277342977&text=cocksuckers
            # Set this to 0 for dev, and 1 for prod

            if (row[2].count(linkcheck)):


#####
# Function monitoring RSS feeds
#####
def rss_monitor(context):
    for name, url_list in rss_dict.items():
        print("Checking for new stuff from ", name, "!")
        requests.get(healthchecker[runningStatus], timeout=10)
        rss_d = feedparser.parse(url_list[0])


def cmd_o365(update, context):
    title[0] = msstatus.find("Title: ", 0, len(msstatus))

    title[1] = msstatus.find("</p>", title[0], impact[0])

    title[2] = msstatus[(title[0] + 7):title[1]]

    tempstat[0] = msstatus.find("ng-binding\">Outlook.com", 0, len(msstatus))
    tempstat[1] = msstatus.find("\" class", tempstat[0], len(msstatus))
    tempstat[2] = msstatus[tempstat[0]:tempstat[1]]
    tempstat[1] = tempstat[2].find("alt=\"")
    servicestatus[0] = tempstat[2][tempstat[1] + 5:len(tempstat[2])]

