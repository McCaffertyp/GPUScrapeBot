import sys
import subprocess

try:
    from selenium import webdriver
except ImportError:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip3', 'install', 'selenium'])
    except subprocess.CalledProcessError:
        print("Error running install command `pip3 install <package>`")
finally:
    from selenium import webdriver

from mccaffertyp.gpu_scraper import GpuScraper

# Variables
user_email = ""
user_password = ""
user_number = ""
user_carrier = ""
user_max_price = ""
user_debit_name = ""
user_debit_number = ""
user_debit_cv = ""


# Actually run the program and print out the prompts
print("___________________________________________________")
print()
print("Please answer the following questions accurately :)")
print()
is_linux = input("Are you using a Linux computer (y/n)? ")
user_wants_messages = input("Do you want text message notifications (y/n)? ")
user_is_buying = input("Do you want the bot to buy for you (y/n)? ")

if is_linux[0] == 'y' or is_linux[0] == 'Y':
    is_linux = True
else:
    is_linux = False
if user_wants_messages[0] == 'y' or user_wants_messages[0] == 'Y':
    user_wants_messages = True
else:
    user_wants_messages = False
if user_is_buying[0] == 'y' or user_is_buying[0] == 'Y':
    user_is_buying = True
else:
    user_is_buying = False

if not user_wants_messages and not user_is_buying:
    print("Why did you even want to use this bot then?")
    print("I'm outta here")
    exit(0)

print("Enter the number of a following option for your browser choice:")
print("1. Chrome (v90 - Windows, v88 - Linux)")
print("2. Firefox (latest - Windows, Linux needs manual)")
print("3. Opera (v90 - Windows, v88 - Linux)")
user_browser = input("Browser choice: ")
sleep_time_seconds = int(input("How often (in seconds) to check websites (default is 5 seconds; enter <1 to keep default)? "))
if sleep_time_seconds < 1:
    sleep_time_seconds = 5

if user_wants_messages:
    user_email = input("What is your gmail (Must be gmail)? ")
    user_password = input("What is your gmail password? ")
    user_number = input("What is your mobile number? ")
    user_carrier = input("What carrier service do you use (Verizon, T-Mobile, etc)? ")
    user_hourly = input("Opting out of below would still allow product in stock updates.\nWould you like hourly updates (y/n)? ")
    if user_hourly[0] == 'y' or user_hourly[0] == 'Y':
        user_hourly = True
    if user_is_buying:
        user_max_price = int(input("What is your max price? "))
        user_debit_name = input("What is the name on your card? ")
        user_debit_number = input("What is your card number? ")
        user_debit_cv = input("What is the cv number? ")
else:
    user_max_price = int(input("What is your max price? "))
    user_debit_name = input("What is the name on your card? ")
    user_debit_number = input("What is your card number? ")
    user_debit_cv = input("What is the cv number? ")

print()
print("Thank you for using GPU Scraping Bot.\nHope you are satisfied with the results :)")
print()
print("___________________________________________________")

gpu_scraper = GpuScraper(is_linux, webdriver, sleep_time_seconds, user_wants_messages, user_is_buying, user_browser,
                         user_email, user_password, user_number, user_carrier, user_max_price,
                         user_debit_name, user_debit_number, user_debit_cv)
gpu_scraper.run()
