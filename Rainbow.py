"""
CSCI 262 - Systems Security
Assignment 1 Question 2

Name: Joen Tai
UOW ID: 7432100
"""
import hashlib
import argparse

# Variables
passDict = {}
RainbowTable = {}
usedPassword = {}

# Part 2 Setup
argName = "CSCI262 Assignment 1 Rainbow Table Generator \t"
argDesc = "Generates a rainbow table when password text file is given"
argParser = argparse.ArgumentParser(prog=argName,description=argDesc)
argParser.add_argument("passwordFile", nargs=1, type=str, help='Enter "Rainbow.py <passwordFile>.txt."')

# Read Args
args = argParser.parse_args()
filename = str(args.passwordFile[0])

# Check if file is valid format
if (not filename.endswith(".txt")):
    print("Please enter a valid .txt file!")
    exit(1)

# Getting total number of words in file
totalLines = 0
with open(filename, "r") as file:
    totalLines = len(file.readlines())

# Adding password to dictionary
with open(filename, "r") as myfile:
    print("Reading passwords in file")
    for line in myfile:
        key = line.strip()
        # Hashing each password and adding to dictionary
        currentHash = hashlib.md5(key.encode()).hexdigest()
        passDict[key] = currentHash

# Functions
def hashChain(password, hashValue):
    tempCount = 0
    # Hash Reduce
    reducedVal = (int(hashValue, 16) % totalLines) + 1
    hv = checkHash(reducedVal)

    # Hash Reduce loop
    while (hv != None):
        tempCount += 1
        currentHash = hv
        reducedVal = (int(currentHash, 16) % totalLines) + 1
        hv = checkHash(reducedVal)

        if (tempCount > 4):
            break
  
    if (hv != None):
        # Adding final hash to rainbow table
        currentHash = hv
        RainbowTable.update({password: hv})

# Searching for next password
def checkHash(reducedVal):
    for i, item in enumerate(passDict):
        if (item not in usedPassword) and (i == (reducedVal - 1)):
            # Marking password as used
            usedPassword.update({item: passDict[item]})
            # Returning hash of next password
            return (passDict[item])
        elif (item in usedPassword) and (i == (reducedVal - 1)):
            # Returning hash of next password
            return (passDict[item])

# Reducing hash for second step
def reducFunc(hashValue):
    reducedVal = (int(hashValue, 16) % totalLines) + 1
    hv = checkHash(reducedVal)
    return (hv)

# Searching for matching hash in rainbow table
def search(rainbowTable, hashValue):
    for item in rainbowTable:
        # Hash found in rainbow table
        if (hashValue in rainbowTable[item]):
            print("\nFound hash in rainbow table!")
            correctPass = matchHash(item, hashValue)
            return(correctPass)
        # Reducing to find hash in rainbow table
        elif (hashValue not in rainbowTable[item]):
            reducePrevHash(rainbowTable[item])

# Reducing to find hash in rainbow table
def reducePrevHash(hashValue):
    print("Searching for original hash")
    counter = 0
    while True:  
        if (hashValue in RainbowTable.values()):
            counter += 1
            hashValue = reducFunc(hashValue)
            if (counter > 10):
                break
        else:
            break

# Finding pre-image
def matchHash(passText, hashValue):
    currentHash = hashlib.md5(passText.encode()).hexdigest()
    # Pre-image found
    if (currentHash == hashValue):
        return (passText)
    else:
        # Reducing to find pre-image
        while True:
            if (currentHash != hashValue):
                currentHash = reducFunc(currentHash)
            else:
                print("The hashes match!")
                return (passText)

# Looping through password list            
for item in passDict:
    # If item in password dictionary is used, continue to next in list
    if (item in usedPassword):
        continue
    else:
        usedPassword.update({item: passDict[item]})
        hashChain(item, passDict[item])

count = 0
# Saving RainbowTable to Rainbow.txt
with open("Rainbow.txt", 'w') as f:
    # Sorting by hash values
    for key, val in sorted(RainbowTable.items(), key = lambda x: x[1]):
        count += 1
        # Writing rainbowtable into text file
        f.write('%s %s\n' % (key, val))
    f.write("Total number of lines in the Rainbow Table is %s" % count)

# Requesting hash value from user
while True:
    inputHash = input('Enter a hash value: ').strip()
    
    # Checking length of string
    if (inputHash.isalnum() == True) and (len(inputHash) == 32):
        # Checking if hash string is valid
        reducedVal = (int(inputHash, 16) % totalLines) + 1
        for i in range (len(inputHash)):
            # Input hash string is invalid
            if (reducedVal == 0):
                print("\nMessage digest string not valid. Please enter hash again.")
            # Input hash string is valid
            elif (i == (len(inputHash) - 1)):
                reducedWord = search(RainbowTable, inputHash)
                if (reducedWord == None):
                    print("Unable to find password in rainbow table.\n")
                else:
                    print("The relative reduced word is: ", reducedWord, "\n")
    elif (len(inputHash) < 32):
        print("\nThe input hash is too short. Please enter hash again.")
    else:
        print("\nInput hash is too long. Please enter hash again.")