import sys
from selenium import webdriver
from time import sleep
import time
from secrets import username, password

# Creates a bot that scrapes craigslist's car+truck section and prints
# ...results to console and cars.txt
class CraigslistBot():
    def __init__(self):
        self.limit = 0
        self.make = ''
        self.cl_driver = webdriver.Chrome()
        self.fb_driver = webdriver.Chrome()
        self.cl_link = 'https://newyork.craigslist.org/search/wch/cta?sort=priceasc&'
        self.fb_link = 'https://www.facebook.com/marketplace/106310892736384/vehicles/?sort=PRICE_ASCEND'
        self.cl_time = 0
        self.fb_time = 0
        self.all_listings = []

    # get input
    def parse_input(self):
        # help output
        if len(sys.argv) <= 1:
            limit = input("Price limit: $")
            make = input("Make (if none, press enter): ")
        # check if make is specified
        elif len(sys.argv) == 2:
            limit = sys.argv[1]
            make = None
        elif len(sys.argv) == 3:
            limit = sys.argv[1]
            make = sys.argv[2]
            
        self.limit = int(limit)
        self.make = make

    # actual get cars function
    def get_cars(self):
        # navigate to craigslist New York, get cars+trucks in ascending order
        self.cl_driver.get(self.cl_link)

        # get start time for timer
        start_time = time.time()

        # open file, begin output line
        print("\n")
        hashes = ""
        for x in range(int(((float(86) - len(" BEGIN LISTINGS ")) / 2))):
            hashes += "#"
        print(hashes + " BEGIN LISTINGS " + hashes + "\n")

        # keep track of price and number of cars
        is_under_price = True
        count = 0
        while(is_under_price):
            # Get list of all listings on current page, increment counter
            cars = self.cl_driver.find_elements_by_class_name('result-row')

            for car in cars:
                # get listing attributes
                price_str = car.find_elements_by_class_name('result-price')[0].text
                price = int(price_str[1:])
                name = car.find_elements_by_class_name('result-title')[0].text
                link = car.find_elements_by_class_name('result-title')[0].get_attribute('href')
                dealership_filter_element = car.find_elements_by_class_name('result-hood')
                if(len(dealership_filter_element) != 0): dealership_filter = dealership_filter_element[0].text
                filter_words = ['finance', 'down', 'payment', 'payments', 'today', 'credit']
                
                # if reached price limit, done
                if price > self.limit:
                    is_under_price = False
                    break

                # if make specified, check
                if self.make != None and self.make.lower() not in name.lower():
                    continue

                # if dealership, skip
                if any(ext in dealership_filter.lower() for ext in filter_words):
                    continue

                # else, add to all_listings array
                price_str = '$' + '{:,.0f}'.format(price)
                tup = ((name, price_str, link), price)
                self.all_listings.append(tup)
                
                # print to console (left align name up to 80 chars, right align price up to 6)
                dots = " "
                for _ in range(79 - len(name)):
                    dots += "."
                console_fmt = '{0:<80}{1:>6}'
                print(console_fmt.format(name + dots, price_str))

                # increment counter
                count += 1
            
            # goto next page
            if(is_under_price):
                self.cl_driver.find_element_by_xpath('//*[@id="searchform"]/div[5]/div[3]/span[2]/a[3]').click()

        # get stop time for timer, assign field
        end_time = time.time()
        total_time = end_time - start_time
        self.cl_time = total_time

        # final output line
        hashes = ""
        for x in range(int(((float(86) - len(" END LISTINGS ")) / 2))):
            hashes += "#"
        print("\n" + hashes + " END LISTINGS " + hashes + "\n")
        # write summary line to file and console, print time elapsed to 2 decimal places
        print("\nFound " + str(count) + " vehicles in " + str(total_time)[:4] + "s.")

    # get cars from Facebook Marketplace
    def get_fb(self):
        # navigate to Facebook Marketplace, get vehicles in ascending order
        self.fb_driver.get(self.fb_link)

        # Login        
        email_field = self.fb_driver.find_element_by_xpath('//*[@id="email"]')
        password_field = self.fb_driver.find_element_by_xpath('//*[@id="pass"]')
        login_btn = self.fb_driver.find_element_by_xpath('//*[@id="loginbutton"]')

        email_field.send_keys(username)
        password_field.send_keys(password)
        login_btn.click()

        # wait for a while
        sleep(2)

        # reload marketplace page (loggin in to fb brings you to timeline)
        self.fb_driver.get(self.fb_link)

        # get start time for timer
        start_time = time.time()

        # keep track of price, number of cars, and Facebook's dynamic array of cars
        is_under_price = True
        count = 0
        iterator = 0
        old_len = 0
        while(is_under_price):
            # Get list of all listings on current page, increment counter
            cars_full_list = self.fb_driver.find_elements_by_class_name('_1oem')
            # while the list hasn't yet updated...
            while old_len == len(cars_full_list):
                # try again...
                cars_full_list = self.fb_driver.find_elements_by_class_name('_1oem')
            
            # Get new list of cars from dynamic list fetched above
            cars = cars_full_list[iterator:iterator+len(cars_full_list)]    
            iterator += len(cars)

            for car in cars:
                # get listing attributes
                price_str = car.find_elements_by_class_name('_f3l')[0].text
                price = int(price_str[1:].replace(',', ''))
                name = car.find_element_by_id('marketplace-modal-dialog-title').get_attribute('title')
                link = car.get_attribute('href')
                
                # if reached price limit, done
                if price > self.limit:
                    is_under_price = False
                    break

                # if make specified, check
                if self.make != None and self.make.lower() not in name.lower():
                    continue

                # add to all_listings array for file output
                tup = ((name, price_str, link), price)
                self.all_listings.append(tup)
                
                # print to console (left align name up to 80 chars, right align price up to 6)
                dots = " "
                for _ in range(79 - len(name)):
                    dots += "."
                console_fmt = '{0:<80}{1:>6}'
                print(console_fmt.format(name + dots, price_str))

                # increment counter
                count += 1
            
            # scroll to bottom of page
            self.fb_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # get stop time for timer, assign field
        end_time = time.time()
        total_time = end_time - start_time
        self.fb_time = total_time

        # final output line
        hashes = ""
        for x in range(int(((float(86) - len(" END LISTINGS ")) / 2))):
            hashes += "#"
        print("\n" + hashes + " END LISTINGS " + hashes + "\n")
        # write summary line to console, print time elapsed to 2 decimal places
        print("\nFound " + str(count) + " vehicles in " + str(total_time)[:4] + "s.")

    # sort all listings by price and put into file
    def sort_and_output(self):
        # sort listings by price
        self.all_listings.sort(key=lambda key: key[1])

        # open file, begin output line
        f = open("cars.txt", "w+")

        # list all cars
        for tup, _ in self.all_listings:
            name, price, link = tup
            file_fmt = '{0:<80}{1:>6} -> {2:<200}\n'
            f.write(file_fmt.format(name, price, link))

        # write summary line
        # f.write("\nFound " + str(count) + " vehicles in " + str(total_time)[:4] + "s.")

        # close file
        f.close()

    # close chrome windows
    def close(self):
        self.cl_driver.quit()
        self.fb_driver.quit()


# create new bot
bot = CraigslistBot()
try:
    # get user input 
    bot.parse_input()
    # scrape website
    bot.get_cars()
    bot.get_fb()
    bot.sort_and_output()
finally:
    # close browser window
    bot.close()