'''
Basic, Native Python
'''

# This is a comment

'''
This is a block comment
It can span multiple lines
'''

# Comments are ignored by Python, so they're just for writing notes to show what your code does



'''
Subject - Syntax Basics
'''
# Programming does numbers a little differently.  Humans start counting at 1, machines start counting at 0.
# So, if you have a list with multiple values, you can show individual values by calling listname[#], where #
# is the number of the entry you want to get.  0 is the first entry.  So, if you had a list with four items, say 10 20 30 and 40.
# listname[0] would be 10, listname[1] would be 20.
# There'll be more on lists later!

# Tabs / Indents

# Python is SUPER SUPER SUPER ANAL about tabs.
# code must be start with no indents.
# Every function or loop ends with a ":", this is when you add a tab to the next line.  For example:
print("Python is easy")
print("Python is easy")

def function():
    # Now we indent
    print("Python is still easy, indents are anal")
    for i in range(0,10):
        # Indent again.
        print("Python is easy")

print("And now we're past that function")

# Basically, the indent tells Python that the indented code belongs specifically to something.
# When we indented after the def function():, that tells Python that all the indented code is part of that function
# It also tells Python that the function ends once it reads a line break that does not have at least one indent.
# The function will include everything from line 23 to line 27, but not line 29.
# It's the same for the for loop, the additional indent after the "for i in range(0,10):" tells the for loop that
# everything with another indent should be run, and then once the next line doesn't have that indent, the code section
# is done and it should step forward in the loop.

# There's more info about loops and functions below, it's okay if those don't make sense.




'''
Subject - Basic Variables
'''

# A variable is a way to store data in the program

# An int is a number, it can be assigned or referenced without any quotes.
var_int = 10

# A string is essentially a list of characters.  Must be enclosed in double or single quotes
var_str = "This is a string"

# A Boolean is just True or False.  The word does not need to be enclosed in quotes.
var_bool_true = True
var_bool_false = False

# A list is a list of values.  Can include multiple types, like int and str
# Access entire list using var_list, access a specific entry with var_list[0], etc
# Empty List:
var_empty_list = []
var_number_list = [0,1,2,3,4,5]
var_str_list = ["FirstVal","SecondVal","ThirdVal"]

# Remember, numbering starts at zero.   So if you want to get the first value of a list, you'd do:
var_str_list[0]
# And the last value, despite there being three values, would be:
var_str_list[2]


# A list within a list
# Access same as list, but with one extra layer.  So var_nested_list[0] for all the entries for the first entry (Even numbers)
# var_nested_list[1] for all the entries in the second entry (odd numbers)
var_nested_list = [[0,2,4,6],[1,3,5,7]]


# Dictionaries

# I never use these, but they're useful for something.
var_dict = {"description":"This is a dictionary","name":"Var Dict"}

# Shows a specific key in the dictionary
var_dict['description']

# Shows everything that is in the dictionary
var_dict.items()




'''
Subject - Variable Interaction
'''

# Variables of different types do not get along well.  For example, if you try to add a str to an int, it will break.
# If you try to print a str and an int together, it will break.
# To fix this, we can use Typecasting.

x = 100
y = "200"   #The quotes make 200 a string, not an int.
z = x+y     # This will net you a "TypeError" error, because you can't add a number and a string of letters together

# To fix this, we typecast y to be an int.  This also works if you typecast x to be a str, but it will give you
# The addition of those two strings, or "100200", which is not really what we want.

z = x + int(y)
z = str(x) + y

# Putting variables into strings

# Say you have a string, like that's part of a call script, and you want to customize it with a user's name
# If the user's name is assigned to the variable "user", you could do this one of two ways.

# Ugly:
# Also requires typecasting if variable is not a string
user = "Jeffery Lebowski"
string = "Hello, "+user+", how is your day today?"
# OR

# A little neater:
user = "Jeffery Lebwoski"
string = f"Hello, {user}, how is your day today?"




'''
Subject - Basic Native Functions
'''

# These are some functions that work out of the box
# First, let's make a variable to manipulate.
var = "Some text"

# len()
## Gets the length of a variable.  If the variable is a list, it will return how many entries there are.
length = len(var)   # This will give length a value of 9

# .replace()
## Can replace any subscrings inside a string with another string
newVar = var.replace("Some ","Stop reading this ")   # This will make newVar equal to "Stop reading this text"

# print() displays information on the console
## You can use one single value, or multiple values.
print("Hello!")     # This prints the string provided
print(var)          # This prints whatever var is equal to
print("Hello!" + var)   # This prints the string "Hello!", along with the value of var.  Using + does not include a space
print("Hello!",var)     # This prints the string "Hello!", along with the value of var.  Using , includes a space between them.

## If you have multiple variable types, you have to typecast them to be the same.  For example:
print("This is a string" + 10)          #   This will fail
print("This is a string" + str(10))     #   This will succeed, because 10 is converted to "10", a string.

# input()
# Asks the user for input

x = input("What is your favorite number?")
print(x)

# .append()
# Adds data to a list
myList = []
data = "One"
myList.append(data)
# myList will now have one entry, "One"

# .lower()
# Turns all letters to lowercase
data = "One"
data = data.lower()
# data will equal "one"

# .upper()
# Just what you'd expect
data = "One"
data = data.upper()
# data will equal "ONE"

'''
Subject - If Statements
'''

# If statements are the easiest way to have the program make decisions based on information.
if 1==1:
    print("Yes, one does in fact equal one")
if 1>0:
    print("One is greater than zero")

# That doesn't make much sense; normally, if statements need to compare variables.  So, for example:
x = 1
if x==1:    #   Evaluates if x is equal to 1.  Since we just set x to 1, this returns as True.
    print("X is equal to one")

# Let's make a nested list, with a user's name and their username
# Then, we'll use an if statement to print the user's username, ONLY if their name is "Jeffery"
#  Basically, an if statement evaluates if something is true.  So, a very basic one:

userdata = [["Jeffery","JLebwoski"],["Donny","TKerabatsos"],["Walter","WSobchak"]]
# Checks the first value of the first sub-list of userdata - or, checks the first value of ["Jeffery","JLebowski"], which is "Jeffery"
# So, if "Jeffery" == "Jeffery" (If one value is equal to another)
#   Do this, which in this case is print the username, or the second value of the first subarray
if userdata[0][0] == "Jeffery":
    print(userdata[0][1])

# Other uses of if:

if "Jeff" in userdata[0][1]:
    print("User's first name contains Jeff")

if userdata[0][0]:
    print("When you just give the if statement a variable, it checks to see if that variable exists")
    print("So, if userdata[0][0] has a value, the if statement will be true, and it will print this data")

# Going further, elif and else
# You can chain commands with elif.

if userdata[0][0] == "Jeffery":
    print("Found Jeffery")
elif userdata[0][0] == "Donny":
    print("Shut the fuck up, Donny")
else:
    print("This code is executed if the above If statements / Elif statements all return false")

'''
Subject - Loops
'''

# Loops are the best way to do a lot of stuff quickly / conceisely.  The biggest one is the For loop, there's also
# while loops

# For Loop
'''
Basic structure:
for something in something else:
    do this
    
Often times when simple for loops are used, that just do something a set number of times, the variable i is used.
Any variable can be used, i is just commonplace.  In the example below, it creates the variable i, and sets it to 
be 0, the first value of the range given.  Then, it executes the code below, which displays the current iteration number
(i), and then says how many iterations before the loop completes.

When the code is finished executing, it increases i by one, and then goes back to the beginning.
'''
for i in range(0,10):
    print("Current iteration number:  " + str(i))
    print("This loop will complete in " + str(10-i) + " iterations.\n")


'''
Iterating through a list:

Instead of using i or some other variable to iterate through a range of numbers,
you can iterate through a list like this.

It's the same concept as i.  The "user" variable can be anything, it could even be i.  But when you use
it in the context "for variable in somelist", it gets assigned each value of the list starting from
0 and ending at the last value.

So, this loop below would draw on the "users" list that is created just above, and print each value individually.
'''
users = ["Jeffery","Donny","Walter"]
for user in users:
    print(user)

# Example, you could also do this below, and get the same results.
# The first variable name does not matter.  This took me a while to understand.
users = ["Jeffery","Donny","Walter"]
for asdegsad44 in users:
    print(asdegsad44)

# You can also do this manually, which is sometimes preferable depending on what you're doing.
users = ["Jeffery","Donny","Walter"]

# This is like the basic for loop, but the range is configure from 0, to whatever the length of the users list is
# Thereby going through the entire list
# users[i] will end up being users[0], users[1], and users[2], stopping after 2, as len(users) will return 3.
for i in range(0,len(users)):
    print(users[i])

# While Loops

# While loops are a little simpler, it essentially means "While this is true, do this".  So:

# This code will set x to 1, and then ask you what you want to set x to.
# As long as you set it to 1, it will keep asking you
# Set it to anything but 1 to break out of the while loop
x = 1
while x == 1:
    x = input("What would you like to make x?")


'''
Subject - Functions
'''
# A function is a collection of code that can be called and run independently, or run and the result set to a variable.
# Most functions begin with "def", then the function name, parenthesis(), and a colon
# Any data or variables that are created inside a function only lives for as long as the function runs.
# Once the function completes, the data is lost.  That's why you need to give data to the functions via the parenthesis,
# and assign the return of the function to a variable to get the result.

# You can use global variables to avoid this, however that takes up more memory among other negatives.

# Function example:
def myFunction():                   # Name the function.  If it requires any input, specify in parenthesis
    print("This is a function")     # Print some data
    return True                     # Return True, to let the user know the function ran.

# Just running a function:
myFunction()

# Running and saving results of function to a variable:
var = myFunction()
print(var)  # This will print True

# Functions can also require input from the user / program.  For example, let's say we have a function that will take a
# string and convert it to be all lowercase.  The function would need to know what string to convert, so we pass it to the
# function inside the parenthesis.
def myFunction(data):       # Name the function, require one input from the code calling the function.  Assign that input to the "data" variable
    data = data.lower()     # Set the data to be all lower case
    return data             # Send the lowercase data back to the program

string = "This is a String with Capital Letters"
lowerstring = myFunction(string)
