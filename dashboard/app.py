# https://coinmarketcap.com/currencies/bitcoin/
# shiny run --reload --launch-browser dashboard/app.py

from bitcoin import get_bitcoin_price, get_bitcoin_market_cap
from ethereum import get_ethereum_price, get_ethereum_market_cap
from dogecoin import get_dogecoin_price, get_dogecoin_market_cap

#print(get_bitcoin_price())

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


@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Get Price Based Off Of User Input
    if str(input.crypto()) == "BTC":
        price = get_bitcoin_price()

    if str(input.crypto()) == "ETH":
        price = get_ethereum_price()

    if str(input.crypto()) == "DOGE":
        price = get_dogecoin_price()

    # Get Market Cap Based Off Of User Input
    if str(input.crypto()) == "BTC":
        market_cap = get_bitcoin_market_cap()

    if str(input.crypto()) == "ETH":
        market_cap = get_ethereum_market_cap()

    if str(input.crypto()) == "DOGE":
        market_cap = get_dogecoin_market_cap()
    
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"price":price, "timestamp":timestamp, "market_cap":market_cap}

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
        def display_price():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['price']}"

    with ui.value_box(
        theme="bg-gradient-blue-purple",  # Change the theme for market cap
    ):
        "Current Market Cap"
        @render.text
        def display_market_cap():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['market_cap']}"

        


#with ui.card(full_screen=True, min_height="40%"):
with ui.card(full_screen=True):
    ui.card_header("Most Recent Prices")

    @render.data_frame
    def display_df():
        """Get the latest reading and return a dataframe with current readings"""
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
        pd.set_option('display.width', None)        # Use maximum width
        return render.DataGrid( df,width="100%")
            
# Reactive observers for either dark mode or light mode
@reactive.effect
def _():
    if input.dark_mode() == "Yes":
        ui.update_dark_mode("dark")
    else:
        ui.update_dark_mode("light")
