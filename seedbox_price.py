#!/usr/sbin/python
import urllib.request, re, sched, time, configparser, smtplib
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('config.ini')

max_price = float(config['DEFAULT']['MaxPriceThreshold'])
min_price = float(config['DEFAULT']['MinPriceThreshold'])
logging = config['DEFAULT'].getboolean('Logging')
pulsedmedia = 'http://pulsedmedia.com'
auctions_page = 'http://pulsedmedia.com/seedbox-auctions.php'
s = sched.scheduler(time.time, time.sleep)

if logging == True:
	f = open('prices.csv','w')
	f.write('Date,OfferLink,Price\n')
	f.close()

def CheckPrice(sc):
	prices_page = urllib.request.urlopen(auctions_page)
	prices_soup = BeautifulSoup(prices_page, 'html.parser')

	price_script = prices_soup.find_all('script', attrs={'language':'javascript'})
	script_split = str(price_script).split('"')
	
	price_lists = [s for s in script_split if "get=price" in s]
	fixed_prices = []
	for x in price_lists:
		fixed_prices.append(x.replace('&amp;', '&'))
		
	for u in fixed_prices:
		page = urllib.request.urlopen(pulsedmedia + u)
		soup = BeautifulSoup(page, 'html.parser')
		near_split = str(soup).split("'")
		final_split = re.sub('[^\d\.]', '', str(near_split[1]))

		if logging == True:
			f = open('prices.csv','a')
			f.write(time.strftime("%d-%m-%Y %H:%M", time.localtime())+','+pulsedmedia+u+','+final_split+'\n')
			f.close()

		if float(final_split) <= max_price and float(final_split) >= min_price:
			print("Current price of " + final_split + "€ is less than the maximum price of " + str(max_price) + "€ and more than the minimum price of " + str(min_price) + "€. Sending an email...")
			email(final_split)
		else:
			print("Current price of " + final_split + "€ does not match the current requests price range, next check in a minute...")

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
