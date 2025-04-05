import streamlit as st
import random
import pandas as pd
import os

st.set_page_config(page_title="ML + DL Matchmaker", page_icon="🎯")

# -------------------------------------
# Leaderboard Handling (in-memory only for Streamlit Cloud)
# -------------------------------------
leaderboard = []

def update_leaderboard(name, score, game_type):
    if name:
        leaderboard.append({"Name": name, "Score": score, "Game": game_type})

def show_leaderboard():
    st.subheader("🏅 Leaderboard (Session Only)")
    if leaderboard:
        df = pd.DataFrame(leaderboard)
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
    if f"score_{game_label}" not in st.session_state:
        st.session_state[f"score_{game_label}"] = 0
        st.session_state[f"round_{game_label}"] = 0
        st.session_state[f"case_{game_label}"] = random.choice(game_cases)

    score = st.session_state[f"score_{game_label}"]
    round_num = st.session_state[f"round_{game_label}"]
    case = st.session_state[f"case_{game_label}"]

    st.markdown(f"### 🔍 Scenario:")
    st.markdown(f"**{case['scenario']}**")

    if game_label == "DL":
        label_map = {"CNN 🖼️": "CNN", "GAN 🎨": "GAN", "Transformer 💬": "Transformer"}
        guess_label = st.radio("Your Guess:", list(label_map.keys()), horizontal=True, key=f"radio_{game_label}_{round_num}")
        guess = label_map[guess_label]
    else:
        guess = st.radio("Your Guess:", choices, horizontal=True, key=f"radio_{game_label}_{round_num}")

    if st.button("Submit", key=f"submit_{game_label}_{round_num}"):
        st.session_state[f"round_{game_label}"] += 1
        if guess == case["answer"]:
            st.success(f"✅ Correct! It's {case['answer']} ({case.get('subtype', case.get('hint', ''))})")
            st.session_state[f"score_{game_label}"] += 1
        else:
            st.error(f"❌ Nope! It was {case['answer']} ({case.get('subtype', case.get('hint', ''))})")

        if st.session_state[f"round_{game_label}"] >= 5:
            st.balloons()
            st.markdown("---")
            name = st.text_input("Enter your name for the leaderboard:", key=f"name_{game_label}_{round_num}")
            if st.button("Submit Score", key=f"submit_score_{game_label}_{round_num}"):
                update_leaderboard(name, st.session_state[f"score_{game_label}"], game_label)
                st.success("Score submitted!")

            rank = "🎓 Rookie"
            if st.session_state[f"score_{game_label}"] >= 4:
                rank = "🏆 Pro"
            elif st.session_state[f"score_{game_label}"] >= 2:
                rank = "💼 Explorer"
            st.markdown(f"### Your Rank: {rank}")
            st.markdown(f"**Final Score: {st.session_state[f'score_{game_label}']} / 5**")

            if st.button("Play Again", key=f"replay_{game_label}_{round_num}"):
                st.session_state[f"score_{game_label}"] = 0
                st.session_state[f"round_{game_label}"] = 0
                st.session_state[f"case_{game_label}"] = random.choice(game_cases)
        else:
            st.session_state[f"case_{game_label}"] = random.choice(game_cases)

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
