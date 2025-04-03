import streamlit as st
import random
import time
from utils.game_logic import (
    get_valid_word,
    get_hint,
    is_valid_word,
    get_definition,
    load_word_list,
)

# Load word lists
word_list = load_word_list()
if "game_mode" not in st.session_state:
    st.session_state.game_mode = "classic"

# Tabs
tabs = st.tabs(["Classic Mode", "MCU Mode"])

# === CLASSIC MODE === #
with tabs[0]:
    st.title("🧠 Theo’s Word Game – Classic Mode")

    if "game_log" not in st.session_state:
        st.session_state.game_log = []
        st.session_state.current_letter = None
        st.session_state.score = 0
        st.session_state.timer_start = None
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
        st.markdown(f"**App's word:** `{st.session_state.app_word}`")

    # Start turn
    with st.form("word_turn"):
        word = st.text_input("Your word:")
        submitted = st.form_submit_button("Submit")

        if submitted and word:
            word = word.strip().lower()

            # Check starting letter
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

                # App responds
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

# === MCU MODE STUB === #
with tabs[1]:
    st.title("🦸 Theo’s Word Game – MCU Mode")
    st.markdown("Coming soon: battle Iron Man, Hulk, and Thanos with Marvel words! BRING MEEEEE THANOSSSSSS!!!")
