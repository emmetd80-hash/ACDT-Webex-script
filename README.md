ACDT Webex Country Info Bot 🌍

A Python bot that listens to messages in a Webex space and returns live country information using multiple public APIs.
Simply type a message in the format:
/CountryName

Example:
"/South Korea"

The bot retrieves data from 4 different APIs and responds automatically in the Webex space.

🚀 Features

When a user types /Country, the bot returns:

1️⃣ Country Information (RestCountries API)

    Official country name

    Capital city

    Population

    Region

    Currency code

2️⃣ Live Weather (OpenWeather API)

    Current temperature
    
    Feels-like temperature
    
    Humidity
    
    Wind speed
    
    Weather conditions

3️⃣ Currency Exchange Rate (open.er-api.com)

    Conversion rate between local currency and GBP

4️⃣ Latest News Headlines (NewsAPI)

    Top 3 news articles related to the country
    
    Includes title + hyperlink to source

5️⃣ Historical Population Graph (API Ninjas)

    Fetches population data from 2005 onward
    
    Interpolates missing years
    
    Generates a scatter plot + trend line
    
    Sends the graph image to Webex

🧠 How It Works

    The bot connects to a Webex room using Webex API authentication.
    
    It monitors the space for new messages starting with /.
    
    It extracts the country name and queries the following APIs:
    
    RestCountries → Basic country info
    
    OpenWeather → Weather
    
    ER-API → Currency exchange
    
    NewsAPI → News headlines
    
    API Ninjas → Historical population data
    
    It formats and sends the data back to the Webex room.
    
    A population graph is generated using Matplotlib and sent as an image.
    
    All errors (bad input, missing data, failed API responses) return user-friendly messages.

🔑 API Keys Needed

    API	                Purpose	            Documentation
    Webex Bot Token	    Posting messages	https://developer.webex.com/docs/api
    
    OpenWeather         API	Weather data    https://openweathermap.org/api
    
    NewsAPI	            News headlines	    https://newsapi.org
    
    API Ninjas	        Population data	    https://api-ninjas.com/api


🗂️ Message Format

To get info for a country, type:

    /Japan
    /France
    /Brazil


Invalid input produces helpful errors, for example:

    /
    ⚠️ Enter a country after '/'. Example: /Japan

📸 Example Output
"/South Korea"

<img width="416" height="645" alt="image" src="https://github.com/user-attachments/assets/681ab947-1a4d-4a48-b3ea-b4c7c9a4b065" />

🐛 Troubleshooting

✔ Bot not responding?

    Ensure TARGET_ROOM matches the exact Webex room name
    
    Verify your Webex Bot token has not expired
    
    Check internet connection or firewall restrictions

✔ Some data missing?

    APIs may occasionally return:
    
    404 (country not found)
    
    429 (rate limit exceeded)
    
    401 (API key invalid)

The bot handles these gracefully and returns readable messages.

✔ Population graph not showing?

    Some countries lack historical population data (e.g., Antarctica).
    The bot will report this instead of failing.

🛠 Future Improvements (Optional)

    Add support for regional abbreviations (/UK, /USA)
    
    Cache API results to reduce rate-limiting
    
    Add slash commands like /help or /about
    
    Add error logging to file

