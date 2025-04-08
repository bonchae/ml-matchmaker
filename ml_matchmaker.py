import streamlit as st
import pandas as pd

st.set_page_config(page_title="ML + DL Matchmaker", page_icon="🎯")

# Initialize session state variables
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.ml_score = 0
    st.session_state.ml_current_question = 0
    st.session_state.dl_score = 0
    st.session_state.dl_current_question = 0
    st.session_state.leaderboard = []

# -------------------------------------
# ML Game Questions
# -------------------------------------
ml_cases = [
    {"scenario": "Spotify Listener Segments", "answer": "Unsupervised", "subtype": "Clustering"},
    {"scenario": "Amazon Demand Forecasting", "answer": "Supervised", "subtype": "Regression"},
    {"scenario": "Gmail Spam Filter", "answer": "Supervised", "subtype": "Classification"},
    {"scenario": "Netflix Recommendation System", "answer": "Unsupervised", "subtype": "Dimensionality Reduction"},
    {"scenario": "Credit Card Fraud Detection", "answer": "Unsupervised", "subtype": "Clustering"},
]

# -------------------------------------
# DL Game Questions
# -------------------------------------
dl_cases = [
    {"scenario": "Google Lens recognizes a plant", "answer": "CNN", "hint": "🖼️ Image classifier"},
    {"scenario": "DALL·E generates pizza ad art", "answer": "GAN", "hint": "🎨 Image generator"},
    {"scenario": "ChatGPT writes emails", "answer": "Transformer", "hint": "💬 Text generator"},
    {"scenario": "Face ID unlocks your phone", "answer": "CNN", "hint": "🖼️ Facial recognition"},
    {"scenario": "Midjourney creates AI artwork", "answer": "GAN", "hint": "🎨 AI Art"},
]

# -------------------------------------
# Update leaderboard function
# -------------------------------------
def update_leaderboard(name, score, game_type):
    if name:
        st.session_state.leaderboard.append({"Name": name, "Score": score, "Game": game_type})

# -------------------------------------
# Show leaderboard function
# -------------------------------------
def show_leaderboard():
    st.subheader("🏅 Leaderboard (Session Only)")
    if st.session_state.leaderboard:
        df = pd.DataFrame(st.session_state.leaderboard)
        top_scores = df.sort_values(by="Score", ascending=False).head(10)
        st.dataframe(top_scores)
    else:
        st.info("No leaderboard data yet. Be the first!")

# -------------------------------------
# ML Game Logic
# -------------------------------------
def run_ml_game():
    if st.session_state.ml_current_question >= len(ml_cases):
        show_ml_results()
        return

    current_case = ml_cases[st.session_state.ml_current_question]
    
    st.markdown(f"### 🔍 Scenario {st.session_state.ml_current_question + 1} of {len(ml_cases)}:")
    st.markdown(f"**{current_case['scenario']}**")
    
    guess = st.radio(
        "Your Guess:", 
        ["Supervised", "Unsupervised", "I'm not sure 🤔"], 
        key=f"ml_radio_{st.session_state.ml_current_question}"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("Submit", key=f"ml_submit_{st.session_state.ml_current_question}"):
            if guess == current_case["answer"]:
                st.session_state.ml_score += 1
                st.success(f"✅ Correct! It's {current_case['answer']} ({current_case['subtype']})")
            else:
                st.error(f"❌ Nope! It was {current_case['answer']} ({current_case['subtype']})")
            
            # Show the Next button after submission
            st.session_state[f"ml_answered_{st.session_state.ml_current_question}"] = True
    
    # Only show Next button after answering
    if st.session_state.get(f"ml_answered_{st.session_state.ml_current_question}", False):
        with col2:
            if st.button("Next Question", key=f"ml_next_{st.session_state.ml_current_question}"):
                st.session_state.ml_current_question += 1
                st.experimental_rerun()

# -------------------------------------
# DL Game Logic
# -------------------------------------
def run_dl_game():
    if st.session_state.dl_current_question >= len(dl_cases):
        show_dl_results()
        return

    current_case = dl_cases[st.session_state.dl_current_question]
    
    st.markdown(f"### 🔍 Scenario {st.session_state.dl_current_question + 1} of {len(dl_cases)}:")
    st.markdown(f"**{current_case['scenario']}**")
    
    label_map = {"CNN 🖼️": "CNN", "GAN 🎨": "GAN", "Transformer 💬": "Transformer"}
    guess_label = st.radio(
        "Your Guess:", 
        list(label_map.keys()), 
        horizontal=True, 
        key=f"dl_radio_{st.session_state.dl_current_question}"
    )
    guess = label_map[guess_label]
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("Submit", key=f"dl_submit_{st.session_state.dl_current_question}"):
            if guess == current_case["answer"]:
                st.session_state.dl_score += 1
                st.success(f"✅ Correct! It's {current_case['answer']} ({current_case['hint']})")
            else:
                st.error(f"❌ Nope! It was {current_case['answer']} ({current_case['hint']})")
            
            # Show the Next button after submission
            st.session_state[f"dl_answered_{st.session_state.dl_current_question}"] = True
    
    # Only show Next button after answering
    if st.session_state.get(f"dl_answered_{st.session_state.dl_current_question}", False):
        with col2:
            if st.button("Next Question", key=f"dl_next_{st.session_state.dl_current_question}"):
                st.session_state.dl_current_question += 1
                st.experimental_rerun()

# -------------------------------------
# Results Display
# -------------------------------------
def show_ml_results():
    st.balloons()
    st.markdown("---")
    
    rank = "🎓 Rookie"
    if st.session_state.ml_score >= 4:
        rank = "🏆 Pro"
    elif st.session_state.ml_score >= 2:
        rank = "💼 Explorer"
    
    st.markdown(f"### Your Rank: {rank}")
    st.markdown(f"**Final Score: {st.session_state.ml_score} / {len(ml_cases)}**")
    
    name = st.text_input("Enter your name for the leaderboard:", key="ml_name_input")
    
    if st.button("Submit Score", key="ml_submit_score"):
        update_leaderboard(name, st.session_state.ml_score, "ML")
        st.success("Score submitted!")
    
    if st.button("Play Again", key="ml_play_again"):
        st.session_state.ml_score = 0
        st.session_state.ml_current_question = 0
        st.experimental_rerun()

def show_dl_results():
    st.balloons()
    st.markdown("---")
    
    rank = "🎓 Rookie"
    if st.session_state.dl_score >= 4:
        rank = "🏆 Pro"
    elif st.session_state.dl_score >= 2:
        rank = "💼 Explorer"
    
    st.markdown(f"### Your Rank: {rank}")
    st.markdown(f"**Final Score: {st.session_state.dl_score} / {len(dl_cases)}**")
    
    name = st.text_input("Enter your name for the leaderboard:", key="dl_name_input")
    
    if st.button("Submit Score", key="dl_submit_score"):
        update_leaderboard(name, st.session_state.dl_score, "DL")
        st.success("Score submitted!")
    
    if st.button("Play Again", key="dl_play_again"):
        st.session_state.dl_score = 0
        st.session_state.dl_current_question = 0
        st.experimental_rerun()

# -------------------------------------
# Main UI
# -------------------------------------
st.title("🎯 Matchmaker: ML & DL Edition")
tabs = st.tabs(["🧮 ML Matchmaker", "🧠 DL Matchmaker", "📊 Leaderboard"])

with tabs[0]:
    run_ml_game()

with tabs[1]:
    run_dl_game()

with tabs[2]:
    show_leaderboard()