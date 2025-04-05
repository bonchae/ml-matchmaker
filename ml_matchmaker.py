import streamlit as st
import random

# Use case list
use_cases = [
    {"scenario": "Spotify Listener Segments", "answer": "Unsupervised", "subtype": "Clustering"},
    {"scenario": "Amazon Demand Forecasting", "answer": "Supervised", "subtype": "Regression"},
    {"scenario": "Gmail Spam Filter", "answer": "Supervised", "subtype": "Classification"},
    {"scenario": "Netflix Recommendation System", "answer": "Unsupervised", "subtype": "Dimensionality Reduction"},
    {"scenario": "Credit Card Fraud Detection", "answer": "Unsupervised", "subtype": "Clustering"},
]

st.set_page_config(page_title="ML Matchmaker", page_icon="🤖")

st.title("🤖 ML Matchmaker: Help the CEO Pick the Right Tool!")
st.subheader("Guess whether the business problem uses Supervised or Unsupervised Learning")

if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.rounds = 0
    st.session_state.case = random.choice(use_cases)

case = st.session_state.case

st.markdown(f"### 🚀 Business Scenario:\n**{case['scenario']}**")

guess = st.radio("What kind of ML is this?", ["Supervised", "Unsupervised", "I'm not sure 🤔"])

if st.button("Submit"):
    st.session_state.rounds += 1
    correct = case["answer"]
    subtype = case["subtype"]
    
    if guess == "I'm not sure 🤔":
        st.warning(f"🤔 No worries! It was **{correct}** Learning ({subtype}).")
    elif guess == correct:
        st.success(f"✅ Correct! It’s **{correct}** Learning ({subtype}).")
        st.session_state.score += 1
    else:
        st.error(f"❌ Nope. It was **{correct}** Learning ({subtype}).")

    if st.session_state.rounds < 5:
        st.session_state.case = random.choice(use_cases)
        st.button("Next Question", on_click=lambda: None)
    else:
        st.markdown("### 🎉 Game Over!")
        st.write(f"Your Score: {st.session_state.score} / 5")
        rank = "🎓 Rookie"
        if st.session_state.score >= 4:
            rank = "🏆 Chief Data Officer"
        elif st.session_state.score >= 2:
            rank = "💼 ML Associate"
        st.markdown(f"**Your Rank: {rank}**")
        if st.button("Play Again"):
            st.session_state.score = 0
            st.session_state.rounds = 0
            st.session_state.case = random.choice(use_cases)
