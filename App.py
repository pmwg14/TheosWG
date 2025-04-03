import streamlit as st
import random
import time
import json
from utils.game_logic import (
    get_valid_word,
    get_hint,
    is_valid_word,
    get_definition,
    load_word_list,
)

st.set_page_config(page_title="Theo’s Word Game", page_icon="🧠")

# Load word lists
word_list = load_word_list()
with open("assets/mcu_words.json", "r") as f:
    mcu_words = json.load(f)

# Tabs
tabs = st.tabs(["Classic Mode", "MCU Mode"])

# === CLASSIC MODE === #
with tabs[0]:
    st.title("🧠 Theo’s Word Game – Classic Mode")

    if "game_log" not in st.session_state:
        st.session_state.game_log = []
        st.session_state.current_letter = None
        st.session_state.score = 0
        st.session_state.app_word = None

    def reset_game():
        st.session_state.game_log = []
        st.session_state.current_letter = None
        st.session_state.score = 0
        st.session_state.app_word = None

    st.button("🔄 New Game", on_click=reset_game)

    if not st.session_state.game_log:
        st.info("Your turn! Start with any word.")
    else:
        st.markdown("### App's Last Word")
        if st.session_state.app_word:
            st.success(f"`{st.session_state.app_word}`")
        else:
            st.success("The app couldn't go — you win!")

    # Input section
    with st.form("word_turn"):
        word = st.text_input("Your word:")
        submitted = st.form_submit_button("Submit")

        if submitted and word:
            word = word.strip().lower()

            if st.session_state.current_letter and not word.startswith(st.session_state.current_letter):
                st.error(f"Word must start with `{st.session_state.current_letter.upper()}`")
            elif not is_valid_word(word, word_list, st.session_state.game_log):
                st.error("Invalid word or already used.")
            else:
                st.session_state.game_log.append(word)
                st.session_state.score += 1
                if len(word) >= 8:
                    st.session_state.score += 1

                st.session_state.current_letter = word[-1]

                app_word = get_valid_word(st.session_state.current_letter, word_list, st.session_state.game_log)
                if app_word:
                    st.session_state.app_word = app_word
                    st.session_state.game_log.append(app_word)
                    st.session_state.current_letter = app_word[-1]
                else:
                    st.success("You win! The app couldn't think of a word!")
                    st.session_state.score += 1
                    st.session_state.app_word = None
                    st.session_state.current_letter = None

    # Tools and scoreboard
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💡 Hint"):
            hints = get_hint(st.session_state.current_letter, word_list, st.session_state.game_log)
            st.info(", ".join(hints[:3]) if hints else "No hints available!")

    with col2:
        if st.session_state.app_word and st.button("📖 Definition"):
            definition = get_definition(st.session_state.app_word)
            st.markdown(definition or "Couldn't find definition!")

    with col3:
        st.metric("Score", st.session_state.score)

    st.markdown("### Game Log")
    st.write(" ➡️ ".join(st.session_state.game_log))

# === MCU MODE === #
with tabs[1]:
    st.title("🦸 Theo’s Word Game – MCU Mode")

    # Session setup
    if "mcu_game_log" not in st.session_state:
        st.session_state.mcu_game_log = []
        st.session_state.mcu_current_letter = None
        st.session_state.mcu_app_word = None
        st.session_state.mcu_score = 0

    def reset_mcu():
        st.session_state.mcu_game_log = []
        st.session_state.mcu_current_letter = None
        st.session_state.mcu_app_word = None
        st.session_state.mcu_score = 0

    st.button("🔁 Start New MCU Battle", on_click=reset_mcu)

    st.markdown("### Theo vs Marvel AI")
    if not st.session_state.mcu_game_log:
        st.info("Begin with any Marvel-related word.")
    else:
        st.markdown("### App's Last Hero Move")
        if st.session_state.mcu_app_word:
            st.success(f"🦹 `{st.session_state.mcu_app_word}`")
        else:
            st.success("🧨 The Multiverse collapsed — you win!")

    with st.form("mcu_turn"):
        word = st.text_input("Enter your MCU word:")
        submitted = st.form_submit_button("Submit")

        if submitted and word:
            word = word.strip().lower()

            if st.session_state.mcu_current_letter and not word.startswith(st.session_state.mcu_current_letter):
                st.error(f"Your word must start with `{st.session_state.mcu_current_letter.upper()}`")
            elif word not in mcu_words or word in st.session_state.mcu_game_log:
                st.error("Not a valid MCU word or already used!")
            else:
                st.session_state.mcu_game_log.append(word)
                st.session_state.mcu_score += 1
                st.session_state.mcu_current_letter = word[-1]

                # App responds
                candidates = [w for w in mcu_words if w.startswith(st.session_state.mcu_current_letter) and w not in st.session_state.mcu_game_log]
                if candidates:
                    app_word = random.choice(candidates)
                    st.session_state.mcu_app_word = app_word
                    st.session_state.mcu_game_log.append(app_word)
                    st.session_state.mcu_current_letter = app_word[-1]
                    st.info(f"⚡ Marvel AI responds: `{app_word}`")
                else:
                    st.balloons()
                    st.success("THEO WINS! Thanos is defeated again!")
                    st.session_state.mcu_app_word = None
                    st.session_state.mcu_current_letter = None
                    st.session_state.mcu_score += 1

    st.metric("Your Score", st.session_state.mcu_score)
    st.markdown("### Battle Log")
    st.write(" ➡️ ".join(st.session_state.mcu_game_log))