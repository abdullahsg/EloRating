import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

# Load match data
@st.cache_data
def load_data():
    file_path = 'Elo Ratings - Match Detail.csv'  # Update with your deployment file path
    match_detail = pd.read_csv(file_path, header=1)  # Use 2nd row as header
    # Select only columns A, B, C, D, I, J
    match_detail = match_detail.iloc[:, [0, 1, 2, 3, 8, 9]]
    match_detail.columns = ['Date', 'Player 1', 'Player 2', 'Result', 'Rating After Match P1', 'Rating After Match P2']
    # Ensure 'Result' column is treated as text
    match_detail['Result'] = match_detail['Result'].astype(str)
    return match_detail

# Main app
st.title("Player Match Details")

# Load data
data = load_data()

# Show all data initially
st.write(data)

st.write("Search for matches involving a specific player.")
# Player name input form
with st.form(key='player_form'):
    player_name = st.text_input("Enter Player Name:")
    submit_button = st.form_submit_button(label='Enter')

# Enter button action
if submit_button:
    if player_name:
        player_name_lower = player_name.lower()
        filtered_data = data[data.apply(lambda row: fuzz.partial_ratio(player_name_lower, row['Player 1'].lower()) > 80 or fuzz.partial_ratio(player_name_lower, row['Player 2'].lower()) > 80, axis=1)]
        filtered_data = data[(data['Player 1'].str.contains(player_name, case=False, na=False)) |
                          (data['Player 2'].str.contains(player_name, case=False, na=False))]

        st.write(filtered_data)
    else:
        st.write("Please enter a player name.")
