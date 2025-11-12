# Importing libraries
import requests
import time
import traceback
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# API Keys
WEBEX_TOKEN = "Bearer NGQ4N2I5NWYtY2RjMy00YmIzLTg0MjctYjcxNWVkNzExMzFjOGFlYjUyNjItYjhj_PE93_d68b3fe9-4c07-4dad-8882-3b3fd6afb92d"
TARGET_ROOM = "ACDT_CW1"
OPENWEATHER_API_KEY = "f37ffd63612c870014f4630800229f76"
NEWSAPI_KEY = "aa118f5e9ef5427aaadf35055383d845"
POP_API_KEY = "LWyPROv2gy6DEybg2F/gdg==gUuA79vlm6Y7hVSb"


# Printing messages
def log(msg):
    print(msg)

# Sending messages to Webex
def post_to_webex(message):
    headers = {"Authorization": WEBEX_TOKEN, "Content-Type": "application/json"}
    payload = {"roomId": roomIdToGetMessages, "markdown": message}
    r = requests.post("https://webexapis.com/v1/messages", json=payload, headers=headers)
    log(f"POST → Webex [{r.status_code}]")
    if r.status_code != 200:
        log(f"⚠️ Error posting message: {r.text}")
    return r.status_code == 200


# Sending graphs to Webex
def post_image_to_webex(graph, filename="plot.png"):
    headers = {"Authorization": WEBEX_TOKEN}
    files = {"files": (filename, graph, "image/png")}
    data = {"roomId": roomIdToGetMessages}
    r = requests.post("https://webexapis.com/v1/messages", headers=headers, data=data, files=files)
    log(f"POST image → Webex [{r.status_code}]")


# Getting country info
def get_country_info(country):
    try:
        url = f"https://restcountries.com/v3.1/name/{country}"
        # Waiting for response from the API
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None, f"❌ Could not fetch data for **{country}**. Status code {response.status_code}"
        data = response.json()
        if not isinstance(data, list) or not data:
            return None, f"❌ No data found for **{country}**."
        info = data[0]
        country_name = info.get("name", {}).get("common", country)
        capital = info.get("capital", ["N/A"])[0]
        population = info.get("population", "N/A")
        region = info.get("region", "N/A")
        currencies = info.get("currencies", {})
        currency_code = list(currencies.keys())[0] if currencies else "N/A"
        # Returning content and no error if success
        return {
            "country_name": country_name,
            "capital": capital,
            "population": population,
            "region": region,
            "currency_code": currency_code
        }, None
    # If error return no content and error message
    except Exception as e:
        return None, f"⚠️ Could not fetch country info: {e}"


# Getting weather info
def get_weather_info(capital):
    if capital == "N/A":
        return "⚠️ Weather info not available."
    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={capital}&appid={OPENWEATHER_API_KEY}&units=metric"
        # Waiting for response from the API
        resp = requests.get(weather_url, timeout=10)
        if resp.status_code != 200:
            return f"⚠️ Weather info for {capital} not available."
        w = resp.json()
        temp = w["main"]["temp"]
        feels = w["main"]["feels_like"]
        desc = w["weather"][0]["description"].capitalize()
        humidity = w["main"]["humidity"]
        wind = w["wind"]["speed"]
        return (
            f"\n**Current Weather in {capital}:** ☁️\n"
            f"🌡 **Temperature:**** {temp}°C (feels like {feels}°C)\n"
            f"💧 **Humidity:** {humidity}%\n"
            f"🌬 **Wind Speed:** {wind} m/s\n"
            f"☀️ **Conditions:** {desc}\n"
        )
    except Exception as e:
        return f"⚠️ Could not fetch weather info: {e}"


# Getting exchange rate info
def get_exchange_rate(currency_code):
    if currency_code == "N/A":
        return "⚠️ Exchange rate data not available."
    try:
        exch_url = "https://open.er-api.com/v6/latest/GBP"
        # Waiting for response from the API
        resp = requests.get(exch_url, timeout=10)
        if resp.status_code != 200:
            return f"⚠️ Error fetching exchange rate: {resp.status_code}"
        data = resp.json()
        rate = data.get("rates", {}).get(currency_code)
        if rate:
            return (
                f"\n💱 ****Exchange Rate (vs GBP):****\n"
                f"• 1 GBP = {rate:.4f} {currency_code}\n"
                f"• 1 {currency_code} = {1 / rate:.4f} GBP"
            )
        else:
            return "⚠️ Exchange rate data not available."
    except Exception as e:
        return f"⚠️ Could not fetch exchange rate: {e}"


# Getting news info
def get_latest_news(country, max_articles=3):
    try:
        url = f"https://newsapi.org/v2/top-headlines?q={country}&apiKey={NEWSAPI_KEY}"
        # Waiting for response from the API
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return f"\n⚠️ News info not available (status {resp.status_code})."
        articles = resp.json().get("articles", [])[:max_articles]
        if not articles:
            return "\n⚠️ No news articles found."
        news_text = "\n📰 **Latest News:**\n"
        # Looping through each news article
        for i, article in enumerate(articles, start=1):
            title = article.get("title", "No title")
            url = article.get("url", "")
            news_text += f"{i}. [{title}]({url})\n"
        return news_text
    except Exception as e:
        return f"\n⚠️ Could not fetch news: {e}"


# Getting historical population data and plotting graph
def generate_country_graph(country):
    try:
        url = f"https://api.api-ninjas.com/v1/population?country={country}"
        headers = {'X-Api-Key': POP_API_KEY}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            log(f"⚠️ Failed to fetch historical population: {resp.status_code}")
            return None
        raw_data = resp.json()
        if 'historical_population' not in raw_data:
            log("⚠️ 'historical_population' key not found")
            return None, f"⚠️ No historical population data found for {country}."

        # Filter years from 2005 onwards
        data = [entry for entry in raw_data['historical_population'] if entry['year'] >= 2005]
        if not data:
            log("⚠️ No population data from 2005 onwards")
            return None, f"⚠️ No population data from 2005 onwards found for {country}."

        years = [entry['year'] for entry in data]
        populations = [entry['population'] for entry in data]

        # Sort by year
        years, populations = zip(*sorted(zip(years, populations)))

        # Interpolate missing years for scatter points
        all_years = np.arange(min(years), max(years) + 1)
        all_populations = np.interp(all_years, years, populations)

        degree = 2
        coeffs = np.polyfit(years, populations, degree)
        poly_line = np.polyval(coeffs, all_years)

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.scatter(all_years, all_populations, color='blue', label='Actual Population (Interpolated)')
        plt.plot(all_years, poly_line, color='red', linestyle='-', label='Line of best fit')
        plt.title(f"{country} Historical Population (2005 onwards)")
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Formatting in millions
        plt.gca().get_yaxis().set_major_formatter(
            lambda x, pos: f"{x / 1_000_000:.1f}M"
        )

        # Saving image to memory
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf, None

    except Exception as e:
        log(f"⚠️ Could not generate plot: {e}")
        return None, f"⚠️ Could not generate population plot: {e}"


# Connecting to Webex room
log("Connecting to Webex Teams...")
r = requests.get("https://webexapis.com/v1/rooms", headers={"Authorization": WEBEX_TOKEN})
if r.status_code != 200:
    raise Exception(f"Webex API error: {r.status_code} - {r.text}")
rooms = r.json().get("items", [])
roomIdToGetMessages = None
for room in rooms:
    if room["title"] == TARGET_ROOM:
        roomIdToGetMessages = room["id"]
        log(f"✅ Connected to Webex space: {TARGET_ROOM}")
        break
if roomIdToGetMessages is None:
    raise Exception(f"Could not find Webex room named '{TARGET_ROOM}'")

# Getting the latest message
init_resp = requests.get(
    "https://webexapis.com/v1/messages",
    params={"roomId": roomIdToGetMessages, "max": 1},
    headers={"Authorization": WEBEX_TOKEN}
)
last_message_id = init_resp.json()["items"][0].get("id") if init_resp.status_code == 200 and init_resp.json().get(
    "items") else None
log("\nBot is now listening for any '/<country>' messages in ACDT_CW1\n")

# Bot loop
while True:
    try:
        time.sleep(2)  # Sleeping to reduce the number of API requests
        params = {"roomId": roomIdToGetMessages, "max": 1}
        r = requests.get(
            "https://webexapis.com/v1/messages",
            params=params,
            headers={"Authorization": WEBEX_TOKEN}
        )
        if r.status_code != 200:
            log(f"⚠️ Error fetching messages: {r.text}")
            continue

        items = r.json().get("items", [])
        if not items:
            continue

        # Get the most recent message
        latest_message = items[0]
        message_id = latest_message.get("id")

        # Skip if it's the latest message
        if message_id == last_message_id:
            continue

        # Update last_message_id, so it doesn't get reprocessed
        last_message_id = message_id

        # Extract message text
        message = latest_message.get("text")
        if not message:
            continue
        message = message.strip()
        if not message.startswith("/"):
            continue

        country = message[1:].strip()
        if not country:
            post_to_webex("⚠️ Enter a country after '/'. Example: /Japan")
            continue

        log(f"🌍 Fetching data for: {country}")

        # Calling main function if error return message to webex right away and skip
        country_info, error = get_country_info(country)
        if error:
            post_to_webex(error)
            continue

        # Calling other functions
        weather_text = get_weather_info(country_info["capital"])
        rate_text = get_exchange_rate(country_info["currency_code"])
        news_text = get_latest_news(country)

        # Formatting message before sending to Webex
        message_text = (
            f"**Country Info: {country_info['country_name']}** 🌎\n\n"
            f"🏙 **Capital:** {country_info['capital']}\n"
            f"👥 **Population:** {country_info['population']:,}\n"
            f"🌍 **Region:** {country_info['region']}\n"
            f"💰 **Currency:** {country_info['currency_code']}\n"
            f"{weather_text}"
            f"{rate_text}"
            f"{news_text}\n"
        )
        post_to_webex(message_text)

        # Generating graph and ensuring it's sent last
        graph, graph_error = generate_country_graph(country)
        if graph_error:
            post_to_webex(graph_error)
        elif graph:
            post_image_to_webex(graph)

        log(f"✅ Info for {country_info['country_name']} posted to Webex.\n")

    # If error send back to webex
    except Exception as e:
        log("⚠️ Exception caught:")
        post_to_webex(f"❌ Unable to fetch data.\nError: {e}")
