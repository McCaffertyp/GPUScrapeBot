import sys
import time
import platform
from .scrapers import Scrapers
from .messaging import Message

# 05-07-2021 5:00:00 PM PST = 1620432000 seconds
benchmark_time = 1620432000
system = platform.system()
websites = {
    "Amazon": "https://www.amazon.com/s?k=rtx+3080&i=computers&rh=n%3A284822%2Cp_72%3A1248879011&dc&qid=1620768618&rnid=1248877011&ref=sr_pg_1",
    "BestBuy": "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=category_facet%3DGPUs%20%2F%20Video%20Graphics%20Cards~abcat0507002&sc=Global&st=rtx%203080&type=page&usc=All%20Categories",
    "NewEgg": "https://www.newegg.com/p/pl?N=100007709%20601357247"
}


class GpuScraper:
    def __init__(self, wb, sts, uwm, ub, ue, up, un, uc, ump):
        self.webdriver = wb
        self.sleep_time_seconds = sts
        self.user_wants_messages = uwm
        self.user_browser = ub
        self.user_max_price = ump
        self.msg = Message(ue, up, un, uc)
        self.sent = False
        self.driver = self.get_driver()
        self.handles = {}
        self.out_of_stock = True
        self.items_in_stock = []
        self.item_status = "out of stock"

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
        # Creating all the windows
        # Doing a .get for each website to force wait for browser page to load
        self.driver.get(websites["Amazon"])
        self.driver.execute_script("window.open('about:blank', 'BestBuy')")
        self.driver.switch_to.window("BestBuy")
        self.driver.get(websites["BestBuy"])
        self.driver.execute_script("window.open('about:blank', 'NewEgg')")
        self.driver.switch_to.window("NewEgg")
        self.driver.get(websites["NewEgg"])
        # Adding all the handles to variable
        self.handles["Amazon"] = self.driver.window_handles[0]
        self.handles["BestBuy"] = self.driver.window_handles[1]
        self.handles["NewEgg"] = self.driver.window_handles[2]
        print("Doing one time loading sleep for 5 seconds to ensure windows have loaded")
        time.sleep(5)

    def is_time_hour(self):
        cur_time = int(time.time())
        check_time = 3600 - ((cur_time - benchmark_time) % 3600)
        print("Variable `check_time` currently at {}".format(check_time))

        if check_time >= 3570 and self.sent is False:
            self.sent = True
            return True

        if check_time <= 30:
            self.sent = False

        return False

    def reset(self):
        self.out_of_stock = True
        self.items_in_stock = []

    def run(self):
        print()
        print("********** START **********")
        print()

        self.init_window_handles()
        scrapers = Scrapers(self.driver, self.handles)

        while True:
            try:
                status = "All items are out of stock"
                self.out_of_stock, self.items_in_stock = scrapers.scrape_amazon(self.items_in_stock)
                self.out_of_stock, self.items_in_stock = scrapers.scrape_best_buy(self.items_in_stock)
                self.out_of_stock, self.items_in_stock = scrapers.scrape_new_egg(self.items_in_stock)

                if not self.out_of_stock:
                    status = "There are {} items in stock.\rSending as separate texts.".format(len(self.items_in_stock))
                    self.msg.send_message(status)

                    for item in self.items_in_stock:
                        self.msg.send_message(item)

                if self.is_time_hour():
                    self.msg.send_message(status)

                print("Sleeping for {} second(s)".format(self.sleep_time_seconds), end="", flush=True)
                for i in range(10):
                    print(".", end="", flush=True)
                    time.sleep(self.sleep_time_seconds / 10)
                print()
                self.reset()

            except KeyboardInterrupt:  # Catch Ctrl+C pressed
                break

        print("Done with scraping\nq=Quitting", end="", flush=True)
        for i in range(3):
            print(".", end="", flush=True)
            time.sleep(1)

        self.msg.quit_server()
        exit(0)
