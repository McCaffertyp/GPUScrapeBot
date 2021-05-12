class Scrapers:
    def __init__(self, driver, handles):
        self.driver = driver
        self.handles = handles

    # Only will be scraping the first page, as that will have the most relevant results
    # (Manually checked page 2 and 3 a couple times throughout the day and didn't see
    # anything worth adding into the search).
    def scrape_amazon(self, items_in_stock):
        out_of_stock = True
        print("Scraping Amazon...")
        self.driver.switch_to.window(self.handles["Amazon"])

        try:
            items_all_elements = self.driver.find_elements_by_class_name('sg-col-12-of-20')

            for item in items_all_elements:
                try:
                    item_texts = item.find_elements_by_tag_name('span')
                    full_item_title = item_texts.find_element_by_class_name('a-size-medium').text
                    if "3080" not in full_item_title:
                        continue
                    item_title = item_texts.find_element_by_class_name('a-size-medium').text.partition(' ')[0]
                    item_price = item_texts.find_element_by_class_name('a-offscreen').text
                    items_in_stock.append("{} RTX 3080 in stock at Best Buy for {}".format(item_title, item_price))

                    out_of_stock = False

                except Exception:
                    # Item price is only shown on Amazon if it's in stock, so when the item price is not there
                    # the assumption is that it's not in stock. But this would throw an exception, so just catch
                    # and ignore if the item price isn't found.
                    continue

            if out_of_stock:
                print("Amazon status: All items currently out of stock")

            return out_of_stock, items_in_stock

        except Exception as error:
            print("Error occurred grabbed elements: {}".format(error))
            print("Attempting scrape again")
            self.scrape_amazon(items_in_stock)

    def scrape_best_buy(self, items_in_stock):
        out_of_stock = True
        item_status = "Sold Out"
        print("Scraping Best Buy...")
        self.driver.switch_to.window(self.handles["BestBuy"])

        try:
            item_status_elements = self.driver.find_elements_by_class_name('add-to-cart-button')
            item_name_elements = self.driver.find_elements_by_class_name('sku-header')
            item_price_elements = self.driver.find_elements_by_class_name('priceView-customer-price')

            for i in range(len(item_status_elements)):
                if item_status != item_status_elements[i].text:
                    out_of_stock = False

                    item_title = item_name_elements[i].text.partition(' ')[0]
                    item_price = item_price_elements[i].find_element_by_tag_name('span').text
                    items_in_stock.append("{} RTX 3080 in stock at Best Buy for {}".format(item_title, item_price))

            if out_of_stock:
                print("Best Buy status: All items currently out of stock")

            return out_of_stock, items_in_stock

        except Exception as error:
            print("Error occurred grabbed elements: {}".format(error))
            print("Attempting scrape again")
            self.scrape_best_buy(items_in_stock)

    def scrape_new_egg(self, items_in_stock):
        out_of_stock = True
        item_status = "OUT OF STOCK"
        print("Scraping NewEgg...")
        self.driver.switch_to.window(self.handles["NewEgg"])

        try:
            item_status_elements = self.driver.find_elements_by_class_name('item-promo')
            item_name_elements = self.driver.find_elements_by_class_name('item-title')
            item_price_elements = self.driver.find_elements_by_class_name('price-current')

            for i in range(len(item_status_elements)):
                if item_status != item_status_elements[i].text:
                    out_of_stock = False

                    item_title = item_name_elements[i].text.partition(' ')[0]
                    item_price = item_price_elements[i].text
                    items_in_stock.append("{} RTX 3080 in stock at NewEgg for {}".format(item_title, item_price))

            if out_of_stock:
                print("NewEgg Status: All items currently out of stock")

            return out_of_stock, items_in_stock

        except Exception as error:
            print("Error occurred grabbed elements: {}".format(error))
            print("Attempting scrape again")
            self.scrape_new_egg(items_in_stock)
