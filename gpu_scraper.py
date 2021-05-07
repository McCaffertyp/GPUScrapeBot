import time
from messaging import Message
from selenium.webdriver import Opera

websites = {
    "NewEgg": "https://www.newegg.com/p/pl?N=100007709%20601357247",
    "BestBuy": "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=category_facet%3DGPUs%20%2F%20Video%20Graphics%20Cards~abcat0507002&sc=Global&st=rtx%203080&type=page&usc=All%20Categories"
}
sleep_time_seconds = 15

user_email = ""
user_password = ""
user_number = ""
user_carrier = ""
user_max_price = 1400
user_debit_name = ""
user_debit_number = ""
user_debit_cv = ""


class GpuScraper:
    def __init__(self):
        self.msg = Message(user_email, user_password, user_number, user_carrier)
        self.driver = Opera(executable_path='C:/Users/fifap/OneDrive/Documents/operadriver_win64/operadriver.exe')
        self.handles = {}
        self.out_of_stock = True
        self.items_in_stock = []
        self.item_status = "out of stock"
        self.status = "All items are out of stock"
        self.purchased = False

    def init_window_handles(self):
        self.driver.get(websites["NewEgg"])
        self.handles["NewEgg"] = self.driver.window_handles[0]
        self.driver.execute_script("window.open('{}', 'new window')".format(websites["BestBuy"]))
        self.handles["BestBuy"] = self.driver.window_handles[1]

    def scrape_new_egg(self):
        self.item_status = "OUT OF STOCK"
        self.driver.switch_to.window(self.handles["NewEgg"])
        item_status_elements = self.driver.find_elements_by_class_name('item-promo')
        item_name_elements = self.driver.find_elements_by_class_name('item-title')
        item_price_elements = self.driver.find_elements_by_class_name('price-current')

        for i in range(len(item_status_elements)):
            if self.item_status != item_status_elements[i].text:
                self.out_of_stock = False

                item_title = item_name_elements[i].text.partition(' ')[0]
                item_price = item_price_elements[i].text
                self.items_in_stock.append("{} RTX 3080 in stock at NewEgg for {}".format(item_title, item_price))

    def scrape_best_buy(self):
        self.item_status = "Sold Out"
        self.driver.switch_to.window(self.handles["BestBuy"])
        item_status_elements = self.driver.find_elements_by_class_name('add-to-cart-button')
        item_name_elements = self.driver.find_elements_by_class_name('sku-header')
        item_price_elements = self.driver.find_elements_by_class_name('priceView-customer-price')

        for i in range(len(item_status_elements)):
            if self.item_status != item_status_elements[i].text:
                self.out_of_stock = False

                item_title = item_name_elements[i].text.partition(' ')[0]
                item_price = item_price_elements[i].find_element_by_tag_name('span').text
                self.items_in_stock.append("{} RTX 3080 in stock at Best Buy for {}".format(item_title, item_price))

    def attempt_purchase(self):
        # TODO Run purchasing script here
        self.purchased = True

    def reset(self):
        self.out_of_stock = True
        self.items_in_stock = []
        self.item_status = "out of stock"
        self.status = "All items are out of stock"

    def run(self):
        print()
        print("********** START **********")
        print()

        self.init_window_handles()

        while True:
            self.scrape_new_egg()
            self.scrape_best_buy()

            if not self.out_of_stock:
                self.status = "There are {} items in stock!".format(len(self.items_in_stock))

            self.msg.send_message(self.status)

            for item in self.items_in_stock:
                self.msg.send_message(item)
                if user_is_buying:
                    self.attempt_purchase()
                    if self.purchased:
                        break

            if self.purchased:
                self.status = "A GPU has been successfully purchased. I suggest you stop my program."
                self.msg.send_message(self.status)
                break

            print("Sleeping for {} seconds".format(sleep_time_seconds))
            time.sleep(sleep_time_seconds)
            self.reset()


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

if not user_wants_messages:
    if user_is_buying:
        user_max_price = input("What is your max price? ")
        user_debit_name = input("What is the name on your card? ")
        user_debit_number = input("What is your card number? ")
        user_debit_cv = input("What is the cv number? ")
    else:
        print("What are you even using this bot for?")
        exit(0)
else:
    if user_is_buying:
        user_email = input("What is your gmail (Must be gmail)? ")
        user_password = input("What is your gmail password? ")
        user_number = input("What is your mobile number? ")
        user_carrier = input("What carrier service do you use (Verizon, T-Mobile, etc)? ")
        user_max_price = input("What is your max price? ")
        user_debit_name = input("What is the name on your card? ")
        user_debit_number = input("What is your card number? ")
        user_debit_cv = input("What is the cv number? ")
    else:
        user_email = input("What is your gmail (Must be gmail)? ")
        user_password = input("What is your gmail password? ")
        user_number = input("What is you mobile number? ")
        user_carrier = input("What carrier service do you use (Verizon, T-Mobile, etc)? ")
print()
print("Thank you for using GPU Scraping Bot.\nHope you are satisfied with the results :)")
print()
print("___________________________________________________")

gpu_scraper = GpuScraper()
gpu_scraper.run()
