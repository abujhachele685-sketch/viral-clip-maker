import streamlit as st
from pytubefix import YouTube
import os

st.set_page_config(page_title="AI Viral Clip Maker Pro", page_icon="🎬")
st.title("🎬 AI Viral Clip Maker Pro")

url = st.text_input("YouTube ভিডিওর লিঙ্ক এখানে দিন:")

if st.button("জাদুর মতো ক্লিপ তৈরি করো"):
    if url:
        try:
            with st.spinner("অপেক্ষা করুন..."):
                # 'use_oauth' এবং 'allow_oauth_cache' ইউটিউবের সিকিউরিটি পার হতে সাহায্য করবে
                yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
                video = yt.streams.filter(progressive=True, file_extension='mp4').first()
                out_file = video.download()
                
                st.video(out_file)
                with open(out_file, "rb") as f:
                    st.download_button("ভিডিওটি সেভ করুন", f, file_name="video.mp4")
                st.success("কাজ সম্পন্ন হয়েছে!")
        except Exception as e:
            st.error(f"এরর: {e}")
            
