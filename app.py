# https://coinmarketcap.com/currencies/bitcoin/
# shiny run --reload --launch-browser dashboard/app.py

# --------------------------------------------
# Imports at the top - PyShiny EXPRESS VERSION
# --------------------------------------------

# From shiny, import just reactive and render
from shiny import reactive, render
from pathlib import Path
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

# --------------------------------------------
# Shiny EXPRESS VERSION
# --------------------------------------------

# --------------------------------------------
# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
# --------------------------------------------

UPDATE_INTERVAL_SECS: int = 1

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
global bitcoin1
bitcoin1 = 0

global bitcoin2
bitcoin2 = 0

global bitcoin3
bitcoin3 = 0

global ethcoin1
ethcoin1 = 0

global ethcoin2
ethcoin2 = 0

global ethcoin3
ethcoin3 = 0

global dogecoin1
dogecoin1 = 0

global dogecoin2
dogecoin2 = 0

global dogecoin3
dogecoin3 = 0

def get_bitcoin_price():
    global bitcoin1
    bitcoin = Path(__file__).parent / "BTC-USD.csv"
    df = pd.read_csv(bitcoin)
    latest_price = df['Close'].iloc[bitcoin1 % len(df)]  # Use modulo to wrap around
    bitcoin1 += 1
    return f"${latest_price:,.2f}"

def get_bitcoin_price_float():
    global bitcoin2
    bitcoin = Path(__file__).parent / "BTC-USD.csv"
    df = pd.read_csv(bitcoin)
    value_float = df['Close'].iloc[bitcoin2 % len(df)]  # Use modulo to wrap around
    bitcoin2 += 1
    return value_float

def get_bitcoin_volume():
    global bitcoin3
    bitcoin = Path(__file__).parent / "BTC-USD.csv"
    df = pd.read_csv(bitcoin)
    latest_price = df['Volume'].iloc[bitcoin3 % len(df)]  # Use modulo to wrap around
    bitcoin3 += 1
    return f"${latest_price:,.2f}"

def get_ethereum_price():
    global ethcoin1
    ethcoin = Path(__file__).parent / "ETH-USD.csv"
    df = pd.read_csv(ethcoin)
    latest_price = df['Close'].iloc[ethcoin1 % len(df)]  # Use modulo to wrap around
    ethcoin1 += 1
    return f"${latest_price:,.2f}"

def get_ethereum_price_float():
    global ethcoin2
    ethcoin = Path(__file__).parent / "ETH-USD.csv"
    df = pd.read_csv(ethcoin)
    value_float = df['Close'].iloc[ethcoin2 % len(df)]  # Use modulo to wrap around
    ethcoin2 += 1
    return value_float

def get_ethereum_volume():
    global ethcoin3
    ethcoin = Path(__file__).parent / "ETH-USD.csv"
    df = pd.read_csv(ethcoin)
    latest_price = df['Volume'].iloc[ethcoin3 % len(df)]  # Use modulo to wrap around
    ethcoin3 += 1
    return f"${latest_price:,.2f}"

def get_dogecoin_price():
    global dogecoin1
    dogecoin = Path(__file__).parent / "DOGE-USD.csv"
    df = pd.read_csv(dogecoin)
    latest_price = df['Close'].iloc[dogecoin1 % len(df)]  # Use modulo to wrap around
    dogecoin1 += 1
    return f"${latest_price:,.2f}"

def get_dogecoin_price_float():
    global dogecoin2
    dogecoin = Path(__file__).parent / "DOGE-USD.csv"
    df = pd.read_csv(dogecoin)
    value_float = df['Close'].iloc[dogecoin2 % len(df)]  # Use modulo to wrap around
    dogecoin2 += 1
    return value_float

def get_dogecoin_volume():
    global dogecoin3
    dogecoin = Path(__file__).parent / "DOGE-USD.csv"
    df = pd.read_csv(dogecoin)
    latest_price = df['Volume'].iloc[dogecoin3 % len(df)]  # Use modulo to wrap around
    dogecoin3 += 1
    return f"${latest_price:,.2f}"

@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    float_value = 0
    # Get Price Based Off Of User Input
    if str(input.crypto()) == "BTC":
        price = get_bitcoin_price()
        float_value = get_bitcoin_price_float()
        volume = get_bitcoin_volume()

    if str(input.crypto()) == "ETH":
        price = get_ethereum_price()
        float_value = get_ethereum_price_float()
        volume = get_ethereum_volume()

    if str(input.crypto()) == "DOGE":
        price = get_dogecoin_price()
        float_value = get_dogecoin_price_float()
        volume = get_dogecoin_volume()

    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"price":price, "timestamp":timestamp, "volume":volume, "float":float_value}

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
        "A dashboard showing the daily prices of cryptocurrency over the past month",
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
        "Daily Price"
        @render.text
        def display_price():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['price']}"

    with ui.value_box(
        theme="bg-gradient-blue-purple",  # Change the theme for market cap
    ):
        "Daily Volume"
        @render.text
        def display_volume():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['volume']}"

        


#with ui.card(full_screen=True, min_height="40%"):
with ui.card(full_screen=True):
    ui.card_header("Most Recent Prices")

    @render.data_frame
    def display_df():
        """Get the latest reading and return a dataframe with current readings"""
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
        pd.set_option('display.width', None)        # Use maximum width
        return render.DataGrid( df,width="100%")
    
with ui.card():
    ui.card_header("Chart with Daily Trend in Price Over Past Month")

    @render_plotly
    def display_plot():
        # Fetch from the reactive calc function
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

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
