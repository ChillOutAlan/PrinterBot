# PrinterBot
Bot is used to send notification to Slack when there are issues with Cartridges, Paper Trays, and Other Hardware.

This bot works specifically with the Dell 5130cdn and B4360dn. Scheme fits one color printer and one black and white printer. Information is stored in MariaDB and pulls the database configuration from a seperate text file. Below is the listed modules within the chatbot
- FuzzyWuzzy
- MySQL Client
- SlackClient
- Unicodedata
