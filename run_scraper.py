import sys
import subprocess

try:
    from selenium import webdriver
except ImportError:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip3', 'install', 'selenium'])
    except subprocess.CalledProcessError:
        print("Error running install command `pip3 install selenium`")
finally:
    from selenium import webdriver

from mccaffertyp.gpu_scraper import GpuScraper

# Variables
user_email = ""
user_password = ""
user_number = ""
user_carrier = ""
user_max_price = ""


# Actually run the program and print out the prompts
print("___________________________________________________")
print()
print("Please answer the following questions accurately :)")
print()
user_wants_messages = input("Do you want text message notifications (y/n)? ")

if user_wants_messages[0] == 'y' or user_wants_messages[0] == 'Y':
    user_wants_messages = True
else:
    user_wants_messages = False

if not user_wants_messages:
    print("Why did you even want to use this bot then?")
    print("I'm outta here")
    exit(0)

print("Enter the number of a following option for your browser choice:")
print("1. Chrome (v90 - Windows, v88 - Linux)")
print("2. Firefox (latest - Windows, Linux needs manual)")
print("3. Opera (v90 - Windows, v88 - Linux)")
user_browser = input("Browser choice: ")
print("Check websites info:")
print("Default value is 5 seconds. Enter any number <= 0 for default. Decimals are supported")
print("Highest allowed is 30 (otherwise checking becomes not often enough)")
sleep_time_seconds = float(input("In seconds, how often should I check websites? "))
if sleep_time_seconds <= 0.0:
    print("Using default value of 5.0 seconds")
    sleep_time_seconds = 5.0
elif sleep_time_seconds > 30.0:
    print("Value was greater than 30.0 - using 30.0 seconds")
    sleep_time_seconds = 30.0

if user_wants_messages:
    user_email = input("What is your gmail (Must be gmail)? ")
    user_password = input("What is your gmail password? ")
    user_number = input("What is your mobile number? ")
    user_carrier = input("What carrier service do you use (Verizon, T-Mobile, etc)? ")
    user_hourly = input("Opting out of below would still allow product in stock updates.\nWould you like hourly updates (y/n)? ")
    if user_hourly[0] == 'y' or user_hourly[0] == 'Y':
        user_hourly = True

print()
print("Thank you for using GPU Scraping Bot.\nHope you are satisfied with the results :)")
print()
print("___________________________________________________")

gpu_scraper = GpuScraper(webdriver, sleep_time_seconds, user_wants_messages, user_browser,
                         user_email, user_password, user_number, user_carrier, user_max_price)
gpu_scraper.run()
