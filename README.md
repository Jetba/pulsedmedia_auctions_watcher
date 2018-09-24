# Pulsedmedia_auctions_watcher
A simple script to check PulsedMedia auctions every minute for a seedbox based on price I made for myself.
If a seedbox is found in the given price range, an email is sent.

Current filters only include a minimum price and a maximum price.

## Usage
The script is coded in python 3, and relies on BeautifulSoup4.
Other libraries used are standard python libraries.

To configure the options used, adjust the configuration in config.ini:  
[DEFAULT]  
MaxPriceThreshold - Maximum price for the alert to trigger  
MinPriceThreshold - Minimum price for the alert to trigger  
Logging - Should the price changes be logged to a separate file. Price changes are logged to prices.csv  
[EMAIL]  
Server - SMTP server  
Username - Username for logging in to SMTP server  
Password - Password for logging in to SMTP server  
Email - Email address where the notification email will be sent  


## Other adjustments
By default the script will check every minute of there is a seedbox in the price range. You can adjust this on line 49 of the python script by changing s.enter(60, 1, CheckPrice, (sc,)) to something else, like s.enter(180, 1, CheckPrice, (sc,)) for a check every 3 minutes.

If you wish to disable email notifications, you can comment out line 45.
