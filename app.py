import streamlit as st
from pytube import YouTube
import os

st.title("YouTube Downloader")

url = st.text_input("YouTube URL টা এখানে দিন:")

if url:
    try:
        # এটি দিলে স্ক্রিনে গুগল লগইন কোড আসবে
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        
        st.write(f"ভিডিওর নাম: **{yt.title}**")
        stream = yt.streams.get_highest_resolution()
        
        if st.button("ডাউনলোড শুরু করুন"):
            with st.spinner("ডাউনলোড হচ্ছে..."):
                file_path = stream.download()
                with open(file_path, "rb") as f:
                    st.download_button("ফোনে সেভ করুন", f, file_name=os.path.basename(file_path))
                st.success("সফলভাবে ডাউনলোড হয়েছে!")
    except Exception as e:
        st.error(f"এরর হয়েছে: {e}")
        
