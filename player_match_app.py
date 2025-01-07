import streamlit as st
import pandas as pd

# Load match data
@st.cache_data
def load_data():
    file_path = 'Elo Ratings - Match Detail.csv'  # Update with your deployment file path
    match_detail = pd.read_csv(file_path, header=1)  # Use 2nd row as header
    # Select only columns A, B, C, D, I, J
    match_detail = match_detail.iloc[:, [0, 1, 2, 3,4,5, 8, 9]]
    match_detail.columns = ['Date', 'Player 1', 'Player 2', 'Result','Score P1', 'Score P2', 'Rating After Match P1', 'Rating After Match P2']
    # Ensure 'Result' column is treated as text
    match_detail['Result'] = match_detail['Result'].astype(str)
    return match_detail

# Main app
st.title("Player Match Details")
st.write("Search for matches involving a specific player.")

# Load data
data = load_data()

# Player name input
player_name = st.text_input("Enter Player Name:")

# Filter data for the player
if player_name:
    filtered_data = data[(data['Player 1'].str.contains(player_name, case=False, na=False)) |
                         (data['Player 2'].str.contains(player_name, case=False, na=False))]
    
    if not filtered_data.empty:
        st.write(f"Match records for **{player_name}**:")
        st.dataframe(filtered_data)
    else:
        st.write(f"No matches found for **{player_name}**.")
