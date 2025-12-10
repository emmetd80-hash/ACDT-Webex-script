ACDT Webex Country Info Bot 🌍

A Python bot that listens to messages in a Webex space and returns live country information using multiple public APIs.
Simply type a message in the format:
/CountryName

Example:
/South Korea

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
