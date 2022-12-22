CSCI 262 - Systems Security
Assignment 1 Question 2

Name: Joen Tai
UOW ID: 7432100

Compliation Instructions
To use the program, user must have python version 3 and above to run the program.
User should also have hashlib installed in library as the hashing function uses hashlib.
User should place Rainbow.py and the Passwords.txt in the same folder.
To run program, open cmd in folder and enter "python Rainbow.py <passwordFile>.txt".
Entering "python Rainbow.py -h" will inform you to enter the name of the text file.
After running program, wait while the program reads the Passwords.txt and generates the rainbow table and write it to Rainbow.txt

Reduction Function Implementation
The reduction function takes the hash value of the password and convert it to hexdigest and integer.
The result of the converted hash value will be modded against the total number of words in the Passwords.txt file and + 1.
Example, reducedVal = (converted hash value % total number) + 1

The total number of words in the Passwords.txt file is obtained when the program runs through the file and adding 1 to the counter for each line it iterates through.
From the result obtained, the value will be used to find the next password in the list.



Hashlib documentation
https://docs.python.org/3/library/hashlib.html