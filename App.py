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

# === Load word lists === #
word_list = load_word_list()
with open("assets/mcu_words.json", "r") as f:
    mcu_words = json.load(f)

# === Hero Options === #
heroes = {
    "Spider-Man": "🕸️",
    "Iron Man": "🤖",
    "Scarlet Witch": "🔮",
    "Black Panther": "🖤",
    "Thor": "⚡",
    "Captain Marvel": "🌟",
}

# === Select Tabs === #
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

    if st.session_state.app_word:
        st.markdown("### App’s Word")
        st.success(f"`{st.session_state.app_word}`")

    with st.form("word_turn"):
        word = st.text_input("Your word:")
        submitted = st.form_submit_button("Submit")

        if submitted and word:
            word = word.strip().lower()

            if st.session_state.current_letter and not word.startswith(st.session_state.current_letter):
                st.error(f"Word must start with `{st.session_state.current_letter.upper()}`")
            elif not is_valid_word(word, word_list, st.session_state.game_log):
                st.warning("Hmm, that’s not in the list... but we’ll trust Theo.")
                word_list.append(word)  # Learn the word
                st.session_state.score += 1
            else:
                st.session_state.score += 1
                if len(word) >= 8:
                    st.session_state.score += 1

            st.session_state.game_log.append(word)
            st.session_state.current_letter = word[-1]

            with st.spinner("🤔 Thinking..."):
                time.sleep(random.randint(3, 8))

            app_word = get_valid_word(st.session_state.current_letter, word_list, st.session_state.game_log)
            if app_word:
                st.session_state.app_word = app_word
                st.session_state.game_log.append(app_word)
                st.session_state.current_letter = app_word[-1]
                st.info(f"🧠 App plays: `{app_word}`")
            else:
                st.balloons()
                st.success(random.choice(["Wakanda Forever!", "Bring me THANOSSSS!", "You win!"]))
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

# === MCU MODE === #
with tabs[1]:
    st.title("🦸 Theo’s Word Game – MCU Mode")

    if "mcu_hero" not in st.session_state:
        st.session_state.mcu_hero = None
        st.session_state.mcu_game_log = []
        st.session_state.mcu_current_letter = None
        st.session_state.mcu_app_word = None
        st.session_state.mcu_score = 0

    def reset_mcu():
        st.session_state.mcu_hero = None
        st.session_state.mcu_game_log = []
        st.session_state.mcu_current_letter = None
        st.session_state.mcu_app_word = None
        st.session_state.mcu_score = 0

    st.button("🔁 New Battle", on_click=reset_mcu)

    if not st.session_state.mcu_hero:
        st.markdown("### Choose your hero:")
        hero_choice = st.selectbox("Who will you play as?", list(heroes.keys()))
        if st.button("Confirm Hero"):
            st.session_state.mcu_hero = hero_choice
            st.success(f"{heroes[hero_choice]} You are now {hero_choice}!")
            st.balloons()
            st.stop()

    st.markdown(f"### {heroes[st.session_state.mcu_hero]} Theo vs J.A.R.V.I.S.")

    if st.session_state.mcu_hero in heroes:
    st.markdown(f"### {heroes[st.session_state.mcu_hero]} Theo vs J.A.R.V.I.S.")
        st.success(f"`{st.session_state.mcu_app_word}`")

    with st.form("mcu_turn"):
        word = st.text_input("Your MCU word:")
        submitted = st.form_submit_button("Submit")

        if submitted and word:
            word = word.strip().lower()

            if st.session_state.mcu_current_letter and not word.startswith(st.session_state.mcu_current_letter):
                st.error(f"Must start with `{st.session_state.mcu_current_letter.upper()}`")
            elif word not in mcu_words or word in st.session_state.mcu_game_log:
                st.warning("J.A.R.V.I.S.: 'That’s... debatable. But I’ll allow it.'")
                mcu_words.append(word)
                st.session_state.mcu_score += 1
            else:
                st.session_state.mcu_score += 1

            st.session_state.mcu_game_log.append(word)
            st.session_state.mcu_current_letter = word[-1]

            with st.spinner("🤖 J.A.R.V.I.S. is thinking..."):
                time.sleep(random.randint(3, 8))

            candidates = [w for w in mcu_words if w.startswith(st.session_state.mcu_current_letter)
                          and w not in st.session_state.mcu_game_log]
            if candidates:
                app_word = random.choice(candidates)
                st.session_state.mcu_app_word = app_word
                st.session_state.mcu_game_log.append(app_word)
                st.session_state.mcu_current_letter = app_word[-1]

                # Themed reactions
                if "hulk" in app_word:
                    st.warning("HULK SMASHHHHH!")
                elif "thor" in app_word:
                    st.info("⚡ Thor calls lightning from the Bifrost!")
                elif "stark" in app_word or "iron" in app_word:
                    st.success("Jarvis: 'Mr Stark would approve.'")
                else:
                    quote = random.choice([
                        f"🤖 J.A.R.V.I.S.: 'Interesting... I choose `{app_word}`.'",
                        f"🤖 J.A.R.V.I.S.: 'A logical response: `{app_word}`.'",
                        f"🤖 J.A.R.V.I.S.: 'Let’s proceed with `{app_word}`.'"
                    ])
                    st.info(quote)
            else:
                st.balloons()
                st.success(random.choice([
                    "🖤 Wakanda Forever!",
                    "⚡ Bring me THANOSSS!",
                    "🧠 J.A.R.V.I.S.: 'You win, sir. Well played.'"
                ]))
                st.session_state.mcu_app_word = None
                st.session_state.mcu_current_letter = None

    st.metric("Your Score", st.session_state.mcu_score)
    st.markdown("### Battle Log")
    st.write(" ➡️ ".join(st.session_state.mcu_game_log))