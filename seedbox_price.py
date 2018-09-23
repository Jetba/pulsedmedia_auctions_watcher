#!/usr/sbin/python
import urllib.request, re, sched, time, configparser, smtplib
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('config.ini')

max_price = float(config['DEFAULT']['MaxPriceThreshold'])
min_price = float(config['DEFAULT']['MinPriceThreshold'])
pulsedmedia = 'http://pulsedmedia.com'
auctions_page = 'http://pulsedmedia.com/seedbox-auctions.php'
s = sched.scheduler(time.time, time.sleep)

def CheckPrice(sc):
	prices_page = urllib.request.urlopen(auctions_page)
	prices_soup = BeautifulSoup(prices_page, 'html.parser')

	price_script = prices_soup.find_all('script', attrs={'language':'javascript'})
	script_split = str(price_script).split('"')
	
	price_lists = [s for s in script_split if "get=price" in s]
	fixed_prices = []
	for x in price_lists:
		fixed_prices.append(x.replace('&amp;', '&'))
		
	price_locations = []
	for y in fixed_prices:
		price_locations.append(pulsedmedia + y)

	for u in price_locations:
		page = urllib.request.urlopen(u)
		soup = BeautifulSoup(page, 'html.parser')
		near_split = str(soup).split("'")
		final_split = str(near_split[1]).replace("€", "")

		if float(final_split) <= max_price and float(final_split) >= min_price:
			print("Current price of " + final_split + "€ is less or equal to requested price of " + str(max_price) + "€. Sending an email and waiting 5 minutes before the next check")
			email(final_split)
			s.enter(300, 1, CheckPrice, (sc,))
		else:
			print("Current price of " + final_split + "€ is more than " + str(max_price) + "€. Waiting for better price, next check in a minute...")
			s.enter(60, 1, CheckPrice, (sc,))

def email( price ):
	server = smtplib.SMTP(config['EMAIL']['Server'], 587)
	server.starttls()
	server.login(config['EMAIL']['Username'], config['EMAIL']['Password'])
	msg_template = "Subject: Seedbox available for " + price + "\n\nThere's a seedbox available at your set price or below. http://pulsedmedia.com/seedbox-auctions.php"
	msg = msg_template
	server.sendmail(config['EMAIL']['Email'], config['EMAIL']['Email'], msg)
	server.quit()

s.enter(1, 1, CheckPrice, (s,))
s.run()
