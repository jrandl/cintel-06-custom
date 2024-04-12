# https://coinmarketcap.com/currencies/bitcoin/
# shiny run --reload --launch-browser dashboard/app.py

# --------------------------------------------
# Imports at the top - PyShiny EXPRESS VERSION
# --------------------------------------------

# From shiny, import just reactive and render
from shiny import reactive, render

# From shiny.express, import just ui and inputs if needed
from shiny.express import ui, input

import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats
from shinyswatch import theme

import pyodide.http
from bs4 import BeautifulSoup

# --------------------------------------------
# Shiny EXPRESS VERSION
# --------------------------------------------

# --------------------------------------------
# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
# --------------------------------------------

UPDATE_INTERVAL_SECS: int = 10

# --------------------------------------------
# Initialize a REACTIVE VALUE with a common data structure
# The reactive value is used to store state (information)
# Used by all the display components that show this live data.
# This reactive value is a wrapper around a DEQUE of readings
# --------------------------------------------

DEQUE_SIZE: int = 30
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

# --------------------------------------------
# Initialize a REACTIVE CALC that all display components can call
# to get the latest data and display it.
# The calculation is invalidated every UPDATE_INTERVAL_SECS
# to trigger updates.
# It returns a tuple with everything needed to display the data.
# Very easy to expand or modify.
# --------------------------------------------

async def get_bitcoin_price():
    url = "https://coinmarketcap.com/currencies/bitcoin/"
    response = await pyodide.http.pyfetch(url)
    if response.status != 200:
        raise Exception(f"Error fetching {url}: {response.status}")
    soup = BeautifulSoup(await response.string(), 'html.parser')
    price = soup.find('span', class_='sc-f70bb44c-0 jxpCgO base-text').text
    return price

async def get_bitcoin_market_cap():
    url = "https://coinmarketcap.com/currencies/bitcoin/"
    response = await pyodide.http.pyfetch(url)
    if response.status != 200:
        raise Exception(f"Error fetching {url}: {response.status}")
    soup = BeautifulSoup(await response.string(), 'html.parser')
    market_cap = soup.find('dd', class_='sc-f70bb44c-0 bCgkcs base-text').text
    market_cap = market_cap.split('$')[-1]  # Split by '$' and get the last part
    return '$' + market_cap  # Add '$' back to the beginning

async def get_bitcoin_price_float():
    url = "https://coinmarketcap.com/currencies/bitcoin/"
    response = await pyodide.http.pyfetch(url)
    if response.status != 200:
        raise Exception(f"Error fetching {url}: {response.status}")
    soup = BeautifulSoup(await response.string(), 'html.parser')
    price = soup.find('span', class_='sc-f70bb44c-0 jxpCgO base-text').text
    price = price.replace('$', '').replace(',', '')
    return float(price)




@reactive.calc()
async def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    float_value = 0
    # Get Price Based Off Of User Input
    if str(input.crypto()) == "BTC":
        price = await get_bitcoin_price()
        float_value = await get_bitcoin_price_float()
        market_cap = await get_bitcoin_market_cap()

    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"price":price, "timestamp":timestamp, "market_cap":market_cap, "float":float_value}

    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)

    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    # For Display: Convert deque to DataFrame for display
    df = pd.DataFrame(deque_snapshot)

    # For Display: Get the latest dictionary entry
    latest_dictionary_entry = new_dictionary_entry

    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapshot, df, latest_dictionary_entry




# Define the Shiny UI Page layout
# Call the ui.page_opts() function
# Set title to a string in quotes that will appear at the top
# Set fillable to True to use the whole page width for the UI
ui.page_opts(title="Josiah's Cryptocurrency Dashboard", fillable=True)

# Sidebar is typically used for user interaction/information
# Note the with statement to create the sidebar followed by a colon
# Everything in the sidebar is indented consistently
with ui.sidebar(open="open"):

    ui.h2("Crypto Dashboard", class_="text-center")
    ui.p(
        "A dashboard showing the current prices of cryptocurrency",
        class_="text-center",
    )
    ui.hr()
    ui.input_select(
    "crypto",
    "Choose A Crypto:",
    {
        "Bitcoin Ecosystem": {"BTC": "Bitcoin"},
        "Ethereum Ecosystem": {"ETH": "Ethereum"},
        "Memes": {"DOGE": "Dogecoin"},
    },
)
    
    ui.h6("Links:")
    ui.a(
        "Josiah's GitHub Source",
        href="https://github.com/jrandl/cintel-06-custom",
        target="_blank",
    )

    # Create radio buttons for dark or light mode
    ui.input_radio_buttons("dark_mode", "Dark Mode:", ["Yes", "No"], selected="No")

# In Shiny Express, everything not in the sidebar is in the main panel

with ui.layout_columns():
    with ui.value_box(
        theme="bg-gradient-blue-purple",
    ):
        "Current Price"
        @render.text
        async def display_price():
            deque_snapshot, df, latest_dictionary_entry = await reactive_calc_combined()
            return f"{latest_dictionary_entry['price']}"

    with ui.value_box(
        theme="bg-gradient-blue-purple",  # Change the theme for market cap
    ):
        "Current Market Cap"
        @render.text
        async def display_market_cap():
            deque_snapshot, df, latest_dictionary_entry = await reactive_calc_combined()
            return f"{latest_dictionary_entry['market_cap']}"

        


#with ui.card(full_screen=True, min_height="40%"):
with ui.card(full_screen=True):
    ui.card_header("Most Recent Prices")

    @render.data_frame
    async def display_df():
        """Get the latest reading and return a dataframe with current readings"""
        deque_snapshot, df, latest_dictionary_entry = await reactive_calc_combined()
        pd.set_option('display.width', None)        # Use maximum width
        return render.DataGrid( df,width="100%")
    
with ui.card():
    ui.card_header("Chart with Current Trend in Price")

    @render_plotly
    async def display_plot():
        # Fetch from the reactive calc function
        deque_snapshot, df, latest_dictionary_entry = await reactive_calc_combined()

        # Ensure the DataFrame is not empty before plotting
        if not df.empty:
            # Convert the 'timestamp' column to datetime for better plotting
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            # Create scatter plot for readings
            # pass in the df, the name of the x column, the name of the y column,
            # and more
        
            fig = px.scatter(df,
            x="timestamp",
            y="float",
            title="Price Readings",
            labels={"float": "Price", "timestamp": "Time"},
            color_discrete_sequence=["blue"] )

            # Update layout as needed to customize further
            fig.update_layout(xaxis_title="Time",yaxis_title="Price")

            return fig
            
# Reactive observers for either dark mode or light mode
@reactive.effect
def _():
    if input.dark_mode() == "Yes":
        ui.update_dark_mode("dark")
    else:
        ui.update_dark_mode("light")
