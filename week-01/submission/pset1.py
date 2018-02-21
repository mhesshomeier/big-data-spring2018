# lists
# Create a list with four Strings
first_list = ['this', 'is', 'my','first', 'list']
# print the third item in the list
print(first_list[2])
# print the first and second items in the list
print(first_list[0:2])
# add 'last' to the end of the list
first_list.append('last')
print(first_list)
# print the list length
print(len(first_list))
# replace 'last' with 'new'
first_list[5]='new'
print(first_list)


# strings
# convert into a normal sentence
sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
print(" ".join(sentence_words))
print(sentence_words)
# reverse the list
list.reverse(sentence_words)
print(sentence_words)
# sort the list using default
list.sort(sentence_words)
print(sentence_words)
sorted(sentence_words)
# sorted returns the list sorted without the 'print' command, it's a function so the data must be explicity passed
# list.sort changes the list itself and doesn't print it, it's a method, not a function
# Random functions
#checkout provided random integer function
from random import randint
# this returns random integer: 100 <= number <= 1000
num = randint(100, 1000)
#Create random integer generator with parameters supplied by the user
def int_gen(x,y):
    for i in range(y):
        if i == 1:
            x = 'hey'
    # "return" indicates what values to output
    return x
print(int_gen(100,2))
from random import randint
# create a random integer functions with inputs defined by the user,
#default lower bound is 0
def randominteger(ystringint, xstringint = 0):
    result = randint(xstringint,ystringint)
    print (result)
    return result
# define inputs for the function
xstring = input("Enter lower range limit:-")
ystring = input("Enter upper range limit:-")
#turn those string inputs into integers
xstringint = int(xstring)
ystringint = int(ystring)
#print to test
print(xstring)
print(xstringint)
#run the function to test
randominteger(ystringint,xstringint)
#assert to test
assert(0 <= randominteger(100) <= 100)
assert(50 <= randominteger(100, xstringint = 50) <= 100)
#print the function
print(randominteger(ystringint,xstringint))

# write a function that evaluates the strength of a password
# code adapted from stack overflow forum: https://stackoverflow.com/questions/41117733/validation-a-password-python

def valid_password(password):
    passwordlength = len(password)
    spec_symbol = ['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
    i = 0
    return_val = True
    if passwordlength < 8:
        print("too short")
        return_val=False
    elif passwordlength > 14:
        print("too long")
        return_val=False
    for char in password:
        if char.isdigit():
            i = i + 1
    if i < 2:
        print('the password should have at least two numerals')
        return_val=False
    if not any(char.isupper() for char in password):
        print('the password should have at least one uppercase letter')
        return_val=False
    if not any(char in spec_symbol for char in password):
        print('the password should have at least one of the specified symbols')
        return_val=False
    if return_val==True:
        print('Good Password!')
    if return_val==False:
        print('bad password')
    return return_val
print(valid_password(password))
#create the password input
password = input("Enter a password that is 8-14 characters long, includes at least two numbers, includes at least one uppercase character, and includes at least one special character:-")





# Write a function that returns a string with user inputs

def title_string(x,y):
    book = 'The number {} bestseller today is: {}'.format(x,y)
    return book
#create input for x
x = input("Enter a number:")
y = input("enter a bookname")
print(title_string(x,y))


# create an exponent function
def exp(x,y):
    number = x
    while y > 1:
        number = x * (number)
        y = y - 1
    return number
print(exp(2,10))
