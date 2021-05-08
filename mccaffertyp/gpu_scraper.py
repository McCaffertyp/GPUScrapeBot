import sys
import time
from .messaging import Message

# 05-07-2021 5:00:00 PM = 1620432000 seconds

benchmark_time = 1620432000
cur_time = int(time.time())
check_time = benchmark_time + (3600 - (cur_time - benchmark_time))
sleep_time_seconds = 15
websites = {
    "NewEgg": "https://www.newegg.com/p/pl?N=100007709%20601357247",
    "BestBuy": "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=category_facet%3DGPUs%20%2F%20Video%20Graphics%20Cards~abcat0507002&sc=Global&st=rtx%203080&type=page&usc=All%20Categories"
}

user_browser = ""
user_email = ""
user_password = ""
user_number = ""
user_carrier = ""
user_max_price = 1400
user_debit_name = ""
user_debit_number = ""
user_debit_cv = ""


def get_driver(webdriver):
    browser_option = int(user_browser)
    path = "{}\\driver_executables\\".format(sys.path[0])
    if browser_option == 1:  # Chrome
        return webdriver.Chrome(executable_path='{}{}'.format(path, "chromedriver.exe"))
    elif browser_option == 2:  # Firefox
        return webdriver.Firefox(executable_path='{}{}'.format(path, "geckodriver.exe"))
    elif browser_option == 3:  # Opera
        return webdriver.Opera(executable_path='{}{}'.format(path, "operadriver.exe"))
    else:
        print("Browser choice is not an option. Try again in several years")
        exit(0)


class GpuScraper:
    def __init__(self, webdriver):
        self.msg = Message(user_email, user_password, user_number, user_carrier)
        self.driver = get_driver(webdriver)
        self.handles = {}
        self.out_of_stock = True
        self.items_in_stock = []
        self.item_status = "out of stock"
        self.purchased = False

    def init_window_handles(self):
        self.driver.get(websites["NewEgg"])
        self.handles["NewEgg"] = self.driver.window_handles[0]
        self.driver.execute_script("window.open('{}', 'new window')".format(websites["BestBuy"]))
        self.handles["BestBuy"] = self.driver.window_handles[1]

    def scrape_new_egg(self):
        self.item_status = "OUT OF STOCK"
        self.driver.switch_to.window(self.handles["NewEgg"])
        try:
            item_status_elements = self.driver.find_elements_by_class_name('item-promo')
            item_name_elements = self.driver.find_elements_by_class_name('item-title')
            item_price_elements = self.driver.find_elements_by_class_name('price-current')

            for i in range(len(item_status_elements)):
                if self.item_status != item_status_elements[i].text:
                    self.out_of_stock = False

                    item_title = item_name_elements[i].text.partition(' ')[0]
                    item_price = item_price_elements[i].text
                    self.items_in_stock.append("{} RTX 3080 in stock at NewEgg for {}".format(item_title, item_price))
        except Exception as error:
            print("Error occurred grabbed elements: {}".format(error))
            print("Attempting scrape again")
            self.scrape_new_egg()

    def scrape_best_buy(self):
        self.item_status = "Sold Out"
        self.driver.switch_to.window(self.handles["BestBuy"])
        try:
            item_status_elements = self.driver.find_elements_by_class_name('add-to-cart-button')
            item_name_elements = self.driver.find_elements_by_class_name('sku-header')
            item_price_elements = self.driver.find_elements_by_class_name('priceView-customer-price')

            for i in range(len(item_status_elements)):
                if self.item_status != item_status_elements[i].text:
                    self.out_of_stock = False

                    item_title = item_name_elements[i].text.partition(' ')[0]
                    item_price = item_price_elements[i].find_element_by_tag_name('span').text
                    self.items_in_stock.append("{} RTX 3080 in stock at Best Buy for {}".format(item_title, item_price))
        except Exception as error:
            print("Error occurred grabbed elements: {}".format(error))
            print("Attempting scrape again")
            self.scrape_best_buy()

    def attempt_purchase(self):
        # TODO Run purchasing script here
        self.purchased = True

    def reset(self):
        self.out_of_stock = True
        self.items_in_stock = []
        self.item_status = "out of stock"

    def run(self):
        print()
        print("********** START **********")
        print()

        self.init_window_handles()

        while True:
            status = "All items are out of stock"
            self.scrape_new_egg()
            self.scrape_best_buy()

            if not self.out_of_stock:
                status = "There are {} items in stock.\rSending as separate texts.".format(len(self.items_in_stock))
                self.msg.send_message(status)

                for item in self.items_in_stock:
                    self.msg.send_message(item)
                    if user_is_buying:
                        self.attempt_purchase()
                        if self.purchased:
                            break

            if self.purchased:
                status = "A GPU has been successfully purchased. I suggest you stop my program."
                self.msg.send_message(status)
                break

            # if check_time % 3600 == 0:
            self.msg.send_message(status)

            print("Sleeping for {} seconds".format(sleep_time_seconds))
            time.sleep(sleep_time_seconds)
            self.reset()

        print("Done with scraping\nquitting", end="", flush=True)
        for i in range(3):
            print(".", end="", flush=True)
            time.sleep(1)

        self.msg.quit_server()


# Actually run the program and print out the prompts
print("___________________________________________________")
print()
print("Please answer the following questions accurately :)")
print()
user_wants_messages = input("Do you want text message notifications (y/n)? ")
user_is_buying = input("Do you want the bot to buy for you (y/n)? ")

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
print("1. Chrome (v90)\n2. Firefox (latest)\n3. Opera (v90)")
user_browser = input("Browser choice: ")

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
