import sys
import time
import platform
from .messaging import Message

# 05-07-2021 5:00:00 PM = 1620432000 seconds
benchmark_time = 1620432000
system = platform.system()
websites = {
    "NewEgg": "https://www.newegg.com/p/pl?N=100007709%20601357247",
    "BestBuy": "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=category_facet%3DGPUs%20%2F%20Video%20Graphics%20Cards~abcat0507002&sc=Global&st=rtx%203080&type=page&usc=All%20Categories"
}


def is_time_hour():
    cur_time = int(time.time())
    check_time = 3600 - ((cur_time - benchmark_time) % 3600)
    print("Variable check_time currently at {}".format(check_time))

    if check_time <= 60:
        return True

    return False


class GpuScraper:
    def __init__(self, wb, sts, uwm, uib, ub, ue, up, un, uc, ump, udna, udnu, udcv):
        self.webdriver = wb
        self.sleep_time_seconds = sts
        self.user_wants_messages = uwm
        self.user_is_buying = uib
        self.user_browser = ub
        self.user_max_price = ump
        self.user_debit_name = udna
        self.user_debit_number = udnu
        self.user_debit_cv = udcv
        self.msg = Message(ue, up, un, uc)
        self.driver = self.get_driver()
        self.handles = {}
        self.out_of_stock = True
        self.items_in_stock = []
        self.item_status = "out of stock"
        self.purchased = False

    def get_driver(self):
        browser_option = int(self.user_browser)
        path = "{}\\mccaffertyp\\driver_executables\\".format(sys.path[0])
        driver_extension = ".exe"
        if system == 'Linux':
            path = path.split("\\")
            path = "/".join(path)
            driver_extension = ""
        if browser_option == 1:  # Chrome
            return self.webdriver.Chrome(executable_path='{}{}{}'.format(path, "chromedriver", driver_extension))
        elif browser_option == 2:  # Firefox
            return self.webdriver.Firefox(executable_path='{}{}{}'.format(path, "geckodriver", driver_extension))
        elif browser_option == 3:  # Opera
            return self.webdriver.Opera(executable_path='{}{}{}'.format(path, "operadriver", driver_extension))
        else:
            print("Browser choice is not an option. Try again in several years")
            exit(0)

    def init_window_handles(self):
        print("Initializing windows and handles")
        self.driver.get(websites["NewEgg"])
        self.handles["NewEgg"] = self.driver.window_handles[0]
        self.driver.execute_script("window.open('{}', 'new window')".format(websites["BestBuy"]))
        self.handles["BestBuy"] = self.driver.window_handles[1]
        print("Doing one time loading sleep for 15 seconds to ensure windows load")
        time.sleep(15)  # One time load to ensure windows properly load in

    def scrape_new_egg(self):
        print("Scraping NewEgg...")
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

            if self.out_of_stock:
                print("NewEgg Status: All items currently out of stock")
        except Exception as error:
            print("Error occurred grabbed elements: {}".format(error))
            print("Attempting scrape again")
            self.scrape_new_egg()

    def scrape_best_buy(self):
        print("Scraping Best Buy...")
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

            if self.out_of_stock:
                print("Best Buy status: All items currently out of stock")
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
                    if self.user_is_buying:
                        self.attempt_purchase()
                        if self.purchased:
                            break

            if self.purchased:
                status = "A GPU has been successfully purchased. I suggest you not run my program again."
                self.msg.send_message(status)
                break

            if is_time_hour():
                self.msg.send_message(status)

            print("Sleeping for {} second(s)".format(self.sleep_time_seconds), end="", flush=True)
            for i in range(10):
                print(".", end="", flush=True)
                time.sleep(self.sleep_time_seconds / 10)
            print()
            self.reset()

        print("Done with scraping\nq=Quitting", end="", flush=True)
        for i in range(3):
            print(".", end="", flush=True)
            time.sleep(1)

        self.msg.quit_server()
        exit(0)
