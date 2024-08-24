import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "dbe49d97304543c1b466128ab4338507"
CLIENT_SECRET = "35c8158d0319422ab941545790bbc8c3"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get album cover URL, artist name, and additional track details from Spotify
def get_song_details(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        artist_name = track["artists"][0]["name"]
        track_popularity = track["popularity"]
        track_duration_ms = track["duration_ms"]
        track_duration_min_sec = f"{track_duration_ms // 60000}:{(track_duration_ms % 60000) // 1000:02d}"
        track_preview_url = track["preview_url"]
        is_explicit = track["explicit"]
        return album_cover_url, artist_name, track_popularity, track_duration_min_sec, track_preview_url, is_explicit
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png", artist_name, None, None, None, None

# Function to recommend similar songs
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_details = []
    for i in distances[1:6]:
        song_name = music.iloc[i[0]].song
        artist_name = music.iloc[i[0]].artist
        album_cover_url, artist_name, track_popularity, track_duration_min_sec, track_preview_url, is_explicit = get_song_details(song_name, artist_name)
        recommended_music_details.append((song_name, artist_name, album_cover_url, track_popularity, track_duration_min_sec, track_preview_url, is_explicit))
    return recommended_music_details

# Load data
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set the page layout and title
st.set_page_config(page_title="Prithvi's Music Recommendation System", layout="wide")

# Custom CSS for website
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');
        body {
    background-color: #0d0d0d;
    background-image: url('path-to-your-subtle-pattern.png');
    background-size: cover;
    background-blend-mode: multiply;
    color: #ffffff;
    font-family: 'Nunito', sans-serif;
    animation: fadeIn 1.5s ease-in-out;
}
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .main {
            background-color: #0d0d0d;
            color: #ffffff;
        }
        .header-box {
    background: linear-gradient(45deg, #1c1c1c, #292929); /* Dark background gradient */
    padding: 20px;
    border-radius: 15px;
    border: 2px solid transparent; /* Transparent border to hold the gradient */
    border-image: linear-gradient(135deg, #00FFFF, #FF00FF) 1; /* Gradient border */    
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7); /* Shadow for depth */
    text-align: center;
    margin-bottom: 20px;
    animation: slideIn 1s ease-out;
}
        @keyframes slideIn {
            from { transform: translateY(-30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1); }
        }
        .stButton>button {
            background-color: #282828;
            color: #ffffff;
            font-size: 18px;
            border-radius: 8px;
            padding: 15px 30px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.8);
            transition: all 0.3s ease;
            border: 1px solid #555;
        }
        .stButton>button:hover {
            background-color: #282828; /* Keep the button background same on hover */
            color: #ffffff;
            transform: scale(1.05);
            box-shadow: 0px 0px 20px rgba(0, 191, 255, 0.8); /* Electric blue shadow */
        }
        h1 {
            color: #ffffff;
            font-family: 'Nunito', sans-serif;
            font-weight: normal; /* Changed to normal weight */
            font-size: 48px;
            margin-bottom: 10px;
            animation: fadeInUp 1s ease-in-out; /* Add the fade-in-up animation */
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.7);
        }
        .stSelectbox {
            margin: 0 auto;
            width: 100%;
        }
          .stSelectbox label {
        color: #ffffff !important; /* Keep the label text color as white */
        font-weight: bold !important; /* Keep the text bold */
        margin-bottom: 5px !important; /* Space below the label */
        background: none !important; /* Remove any background */
        padding: 0 !important; /* Remove any padding */
        border: none !important; /* Remove any border */
        box-shadow: none !important; /* Ensure there's no shadow */
        display: block !important; /* Ensure it's displayed as a block element */
    }
        }
       .stSelectbox div {
    background-color: #1a1a1a !important; /* Set background to a very dark gray */
    color: #ffffff !important;
    border-radius: 8px !important; /* Add rounded corners */
    box-shadow: none !important; /* Remove default shadow */
    margin-bottom: 0px !important; /* Remove bottom margin */
    border: none !important; /* Remove default border */
    box-sizing: border-box; /* Ensure padding is included within width/height */
    height: auto !important; /* Adjust height automatically */
    padding: 8px !important; /* Add padding for content spacing */
    display: flex; /* Use flexbox to center content */
    align-items: center; /* Vertically center content */
    font-size: 16.94px !important; /* Maintain increased font size */
    height: 36.3px !important; /* Maintain increased height */
    transition: box-shadow 0.3s ease, border 0.3s ease; /* Smooth transition for hover effects */
}

.stSelectbox div:hover {
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.5) !important; /* Subtle white glow on hover */
    border: none !important; /* Ensure no additional border on hover */
}

.stSelectbox div input {
    background-color: transparent !important; /* Use transparent to avoid layering */
    border: none !important; /* Remove border to prevent multiple borders */
    padding: 0px !important; /* Remove padding inside input */
    font-family: 'Nunito', sans-serif !important;
    font-weight: bold !important;
    font-size: 16.94px !important; /* Maintain increased font size */
    color: #ffffff !important;
    text-align: left !important; /* Align text to the left */
    line-height: normal !important; /* Use normal line-height */
    width: 100%; /* Ensure input uses full width */
    margin: 0 !important;
    height: auto !important; /* Adjust height automatically */
    box-shadow: none !important; /* Ensure no shadow on the input itself */
}

.stSelectbox div input:focus {
    outline: none !important;
    background-color: transparent !important; /* No background on focus */
    border: none !important; /* Ensure no border on focus */
    box-shadow: none !important; /* Ensure no shadow on focus */
}
        }
        .song-title {
            font-weight: normal; /* Changed to normal weight */
            font-family: 'Nunito', sans-serif; /* Ensure the same font-family */
            color: #FF00FF; /* Magenta color */
            text-align: center;
            margin-top: 10px;
            font-size: 18px;
            text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.7);
        }
        .artist-name {
            font-weight: normal; /* Normal weight */
            font-family: 'Nunito', sans-serif; /* Ensure the same font-family */
            color: #a0a0a0; /* Lighter gray color */
            text-align: center;
            margin-top: 5px;
            font-size: 16px;
            text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5);
        }
        .track-info {
            font-weight: normal;
            font-family: 'Nunito', sans-serif;
            color: #ffffff;
            text-align: center;
            margin-top: 5px;
            font-size: 12px;
            text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5);
        }
        img {
            border-radius: 15px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 0 0 rgba(0, 0, 0, 0); /* No shadow by default */
        }
        img:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 12px #00BFFF; /* Electric blue shadow */
        }
        .logo-box {
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #00FFFF, #FF00FF, #800080);
            color: #121212;
            font-family: 'Nunito', sans-serif;
            font-size: 36px;
            font-weight: bold;
            width: 120px;
            height: 120px;
            margin: 0 auto 20px auto;
            border-radius: 15px;
            transform: scale(1.05);
            box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.5); /* Slight glow on hover */
            transition: all 0.3s ease;
            box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.9);
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }
        .recommendation-header {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            margin-top: 40px;
            color: #FF00FF; /* Magenta color */
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.7);
            position: relative;
        }
        .recommendation-header::after {
            content: '';
            display: block;
            width: 60px;
            height: 3px;
            background-color: #00BFFF; /* Electric blue underline */
            margin: 10px auto 0;
        }
        .recommendations {
            display: flex;
            overflow-x: auto;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .recommendations::-webkit-scrollbar {
            height: 8px;
        }
        .recommendations::-webkit-scrollbar-thumb {
            background-color: #FF00FF; /* Magenta scrollbar */
            border-radius: 10px;
        }
        .recommendations::-webkit-scrollbar-track {
            background-color: #222;
            @keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
    .footer {
    background-color: #1a1a1a;
    color: #00FFFF;
    text-align: center;
    padding: 20px;
    font-family: 'Nunito', sans-serif;
    font-size: 12px;
    border-radius: 8px;
    box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.8);
    margin-top: 30px;
    width: 100%; /* Ensure the footer spans the full width */
    box-sizing: border-box; /* Ensure padding is included within width */
    position: fixed; /* Fix the footer at the bottom of the viewport */
    bottom: 0; /* Align the footer to the bottom */
    left: 0; /* Ensure the footer starts from the left edge */
    right: 0; /* Ensure the footer ends at the right edge */
}
    </style>
""", unsafe_allow_html=True)

# Logo container with added depth
st.markdown('<div class="logo-container"><div class="logo-box">PR</div></div>', unsafe_allow_html=True)

# App header inside a fancy box with the updated font style
st.markdown("""
<div class="header-box">
    <h1>Prithvi's Music Recommendation Engine</h1>
</div>
""", unsafe_allow_html=True)

# Selectbox for song selection with updated search box styling
music_list = music['song'].values
selected_song = st.selectbox("Type or select a song from the dropdown", music_list)

# Recommendation button
if st.button('Show Recommendation'):
    recommended_music_details = recommend(selected_song)
    
    st.markdown("<h2 class='recommendation-header'>You Might Also Like</h2>", unsafe_allow_html=True)
    
    # Display recommended songs inside a scrollable container
    st.markdown("<div class='recommendations'>", unsafe_allow_html=True)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            song_name, artist_name, album_cover_url, track_popularity, track_duration_min_sec, track_preview_url, is_explicit = recommended_music_details[idx]
            st.image(album_cover_url, use_column_width=True)
            st.markdown(f"<p class='song-title'>{song_name}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='artist-name'>{artist_name}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='track-info'>Popularity: {track_popularity}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='track-info'>Duration: {track_duration_min_sec}</p>", unsafe_allow_html=True)
            
            # Add "Preview" label above the audio player with grey color and mono font
            if track_preview_url:
                st.markdown("<p class='preview-label' style='text-align: center; color: #6FA8DC; font-family: monospace;'>Preview</p>", unsafe_allow_html=True)
                st.audio(track_preview_url, format="audio/mp3")
            
            if is_explicit:
                st.markdown("<p class='track-info' style='color:red;'>Explicit</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer section
st.markdown("""
<div class="footer" style="color: #808080; font-family: monospace; text-align: center;">
    <p>Created by Prithvi Raj Juloori | © 2024</p>
</div>
""", unsafe_allow_html=True)