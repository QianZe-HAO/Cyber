import pandas as pd
import streamlit as st
import re

def handle_url():
    st.sidebar.markdown("### Append URL")

    # Initialize an empty list to store URLs
    if "url_list" not in st.session_state:
        st.session_state.url_list = []

    # Text input for URL
    new_url = st.sidebar.text_input("Enter a URL")

    # Add the URL to the list when the button is pressed
    if st.sidebar.button("Add URL"):
        if new_url:
            # URL validation using regular expression
            url_pattern = re.compile(
                r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
            )
            if url_pattern.match(new_url):
                if new_url not in st.session_state.url_list:
                    st.session_state.url_list.append(new_url)
                    st.sidebar.success(f"URL added: {new_url}")
                else:
                    st.sidebar.warning("URL already exists.")
            else:
                st.sidebar.error("Please enter a valid URL.")
        else:
            st.sidebar.error("Please enter a valid URL.")

    # Button to delete all URLs
    if st.sidebar.button("Delete All URLs"):
        st.session_state.url_list.clear()
        st.sidebar.success("All URLs deleted.")

    # Display the list of URLs
    if st.session_state.url_list:
        url_df = pd.DataFrame(st.session_state.url_list, columns=["Stored URLs"])
        st.sidebar.dataframe(url_df, width=600, hide_index=True)
    else:
        st.sidebar.warning("No URLs added yet.")

    return st.session_state.url_list