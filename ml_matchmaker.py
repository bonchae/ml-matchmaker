import streamlit as st
import random
import pandas as pd
import os

st.set_page_config(page_title="ML + DL Matchmaker", page_icon="🎯")

# -------------------------------------
# Leaderboard Handling
# -------------------------------------
def update_leaderboard(name, score, game_type, file="leaderboard.csv"):
    entry = pd.DataFrame([[name, score, game_type]], columns=["Name", "Score", "Game"])
    if os.path.exists(file):
        lb = pd.read_csv(file)
        lb = pd.concat([lb, entry], ignore_index=True)
    else:
        lb = entry
    lb.to_csv(file, index=False)

def show_leaderboard(file="leaderboard.csv"):
    if os.path.exists(file):
        st.subheader("🏅 Leaderboard")
        df = pd.read_csv(file)
        top_scores = df.sort_values(by="Score", ascending=False).head(10)
        st.dataframe(top_scores)
    else:
        st.info("No leaderboard data yet. Be the first!")

# -------------------------------------
# ML Game
# -------------------------------------
ml_cases = [
    {"scenario": "Spotify Listener Segments", "answer": "Unsupervised", "subtype": "Clustering"},
    {"scenario": "Amazon Demand Forecasting", "answer": "Supervised", "subtype": "Regression"},
    {"scenario": "Gmail Spam Filter", "answer": "Supervised", "subtype": "Classification"},
    {"scenario": "Netflix Recommendation System", "answer": "Unsupervised", "subtype": "Dimensionality Reduction"},
    {"scenario": "Credit Card Fraud Detection", "answer": "Unsupervised", "subtype": "Clustering"},
]

# -------------------------------------
# DL Game
# -------------------------------------
dl_cases = [
    {"scenario": "Google Lens recognizes a plant", "answer": "CNN", "hint": "🖼️ Image classifier"},
    {"scenario": "DALL·E generates pizza ad art", "answer": "GAN", "hint": "🎨 Image generator"},
    {"scenario": "ChatGPT writes emails", "answer": "Transformer", "hint": "💬 Text generator"},
    {"scenario": "Face ID unlocks your phone", "answer": "CNN", "hint": "🖼️ Facial recognition"},
    {"scenario": "Midjourney creates AI artwork", "answer": "GAN", "hint": "🎨 AI Art"},
]

# -------------------------------------
# Game Logic
# -------------------------------------
def run_game(game_cases, choices, game_label):
    if "score" not in st.session_state:
        st.session_state.score = 0
        st.session_state.round = 0
        st.session_state.case = random.choice(game_cases)

    case = st.session_state.case
    st.markdown(f"### 🔍 Scenario:")
    st.markdown(f"**{case['scenario']}**")

    guess = st.radio("Your Guess:", choices, horizontal=True)

    if st.button("Submit"):
        st.session_state.round += 1
        if guess == case["answer"]:
            st.success(f"✅ Correct! It's {case['answer']} ({case.get('subtype', case.get('hint', ''))})")
            st.session_state.score += 1
        else:
            st.error(f"❌ Nope! It was {case['answer']} ({case.get('subtype', case.get('hint', ''))})")

        if st.session_state.round >= 5:
            st.markdown("---")
            name = st.text_input("Enter your name for the leaderboard:", key=f"name_{game_label}")
            if st.button("Submit Score"):
                update_leaderboard(name, st.session_state.score, game_label)
                st.success("Score submitted!")

            rank = "🎓 Rookie"
            if st.session_state.score >= 4:
                rank = "🏆 Pro"
            elif st.session_state.score >= 2:
                rank = "💼 Explorer"
            st.markdown(f"### Your Rank: {rank}")
            st.markdown(f"**Final Score: {st.session_state.score} / 5**")

            if st.button("Play Again"):
                st.session_state.score = 0
                st.session_state.round = 0
                st.session_state.case = random.choice(game_cases)
        else:
            st.session_state.case = random.choice(game_cases)

# -------------------------------------
# Main Tabs UI
# -------------------------------------
st.title("🎯 Matchmaker: ML & DL Edition")
tabs = st.tabs(["🧮 ML Matchmaker", "🧠 DL Matchmaker", "📊 Leaderboard"])

with tabs[0]:
    run_game(ml_cases, ["Supervised", "Unsupervised", "I'm not sure 🤔"], "ML")

with tabs[1]:
    run_game(dl_cases, ["CNN 🖼️", "GAN 🎨", "Transformer 💬"], "DL")

with tabs[2]:
    show_leaderboard()

