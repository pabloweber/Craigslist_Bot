# Craigslist car+truck Web Scraper

This code uses the Selenium library to scrape vehicle data off of Craigslist's car+truck section.

## Getting Started

First, clone the project.
```
git clone https://github.com/pabloweber/Craigslist_Bot.git
```
Next, install Selenium.
```
pip3 install selenium
```
Finally, run the program.
```
python bot.py [price limit]
```

### Prerequisites

The only prerequisite you need is Selenium. Install it like such:

```
pip3 install selenium
```

## Options
To run a simple search for cars or trucks below a price limit, run:
``` 
python bot.py [price limit]
```
To specify a specific option, run:
```
python bot.py [price limit] [option]
```
For example, to search for Hondas under $2000, run:
```
python bot.py 2000 honda
```
If no price limit is specified as a command line argument, then the user will be prompted for one via input.
```
python bot.py
>> Price limit: $_
```

## Output
After running the program, a list of cars+trucks found will be printed to the console as it searches the website. The program will then exit with a summary line displaying the number of vehicles found, and the total time elapsed.
For example:
```
python bot.py 2000 honda
```
Gives the following output:
```
################################### BEGIN LISTINGS ###################################

2007 honda fit for parts .......................................................  $600
1999 Honda Accord ..............................................................  $900
2015 Honda Pilot 4x4 EX-L ...................................................... $1999
2007 Honda Fit Sport Hatchback ................................................. $1999
2016 Honda Odyssey SE .......................................................... $1999
2016 Honda Civic EX-L With Navigation .......................................... $1999
2016 Honda Pilot All Wheel Drive EX-L .......................................... $1999
2016 Honda CR-V All Wheel Drive SE ............................................. $1999
2005 Honda Accord for sale or Part Out ......................................... $2000

#################################### END LISTINGS ####################################


Found 9 vehicles in 3.70s.
```
The program will also create a file `cars.txt` with a list of all vehicles found, their respective price, and a link to each listing.


## Built With

* [Selenium](https://www.selenium.dev/) - The WebDriver used

## Contributing

Feel free to branch and submit a pull request!

## Authors

* **Pablo Weber** - *University of Virginia 2021* - [LinkedIn](https://www.linkedin.com/in/pabloweber/)

## License

This project is licensed under the MIT License.

