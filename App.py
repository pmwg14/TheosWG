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