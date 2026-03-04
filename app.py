import streamlit as st
import os
from dotenv import load_dotenv
import asyncio

from telegram_scraper import TelegramScraper
from utils import save_csv


st.title("FIU Telegram OSINT Discovery Tool")

api_id = os.getenv("api_id")    #st.text_input("Telegram API ID")
api_hash = os.getenv("api_hash")         #st.text_input("Telegram API HASH")

keywords = st.text_area(
    "Keywords (comma separated)",
    "crypto, hawala, darknet"
)

run = st.button("Start Discovery")

if run:

    kw = [k.strip() for k in keywords.split(",")]

    scraper = TelegramScraper(api_id, api_hash)

    with st.spinner("Searching Telegram..."):

        data = asyncio.run(scraper.run(kw))

    df = save_csv(data)

    st.success(f"Found {len(df)} channels")

    st.dataframe(df)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        file_name="telegram_channels.csv"
    )