# Pulsedmedia_auctions_watcher
A simple script to check PulsedMedia auctions every minute for a seedbox based on price.
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
