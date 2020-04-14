import sys
from selenium import webdriver
import time

class CraigslistBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

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
            
        return (int(limit), make)

    # actual get cars function
    def get_cars(self, limit, make=None):
        # navigate to craigslist New York, get cars+trucks in ascending order
        self.driver.get('https://newyork.craigslist.org/search/wch/cta?sort=priceasc&')

        # get start time for timer
        start_time = time.time()

        # open file, begin output line
        f = open("cars.txt", "w+")
        print("\n")
        hashes = ""
        for x in range(int(((float(86) - len(" BEGIN LISTINGS ")) / 2))):
            hashes += "#"
        print(hashes + " BEGIN LISTINGS " + hashes + "\n")


        is_under_price = True
        count = 0
        while(is_under_price):
            # Get list of all listings on current page, increment counter
            cars = self.driver.find_elements_by_class_name('result-row')

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
                if price > limit:
                    is_under_price = False
                    break

                # if make specified, check
                if make != None and make.lower() not in name.lower():
                    continue

                # if dealership, skip
                if any(ext in dealership_filter.lower() for ext in filter_words):
                    continue

                # else, write to file
                line = [name, " -> ", price_str, " | ", link, "\n"]
                f.writelines(line)
                
                # print to console (left align name up to 80 chars, right align price up to 6)
                dots = " "
                for _ in range(79 - len(name)):
                    dots += "."
                fmt = '{0:<80}{1:>6}'
                print(fmt.format(name + dots, price_str))

                # increment counter
                count += 1
            
            # goto next page
            if(is_under_price):
                self.driver.find_element_by_xpath('//*[@id="searchform"]/div[5]/div[3]/span[2]/a[3]').click()

        # get stop time for timer
        end_time = time.time()
        total_time = end_time - start_time

        # final output line
        hashes = ""
        for x in range(int(((float(86) - len(" END LISTINGS ")) / 2))):
            hashes += "#"
        print("\n" + hashes + " END LISTINGS " + hashes + "\n")
        # write summary line to file and console, print time elapsed to 2 decimal places
        f.write("\nFound " + str(count) + " vehicles in " + str(total_time)[:4] + "s.")
        print("\nFound " + str(count) + " vehicles in " + str(total_time)[:4] + "s.")

        # close file
        f.close()

    # close chrome window
    def close(self):
        self.driver.quit()


        


# call function
bot = CraigslistBot()
limit, make = bot.parse_input()
bot.get_cars(limit, make)
bot.close()