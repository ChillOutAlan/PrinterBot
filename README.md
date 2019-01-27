# PrinterBot
Bot is used to send notification to Slack when there are issues with Cartridges, Paper Trays, and Other Hardware.

This bot works specifically with the Dell 5130cdn and B4360dn. Scheme fits one color printer and one black and white printer. Information is stored in MariaDB and pulls the database configuration from a separate text file. Below is the listed libraries used in the bot:
- FuzzyWuzzy
- MySQL Client
- SlackClient
- Unicodedata
- Requests

MariaDB contains two tables which are BWPRINTER (Black and White Printer B4360dn) and COLORPRINTER (The Color Printer 5130cdn). Each table contains a Date time column which is used for triggering notifications. The columns are NULL by default and will need to have the columns populated with data.
