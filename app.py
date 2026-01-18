import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Viral Clip Maker", page_icon="🎬")
st.title("🎬 Viral Clip Maker (New Method)")

url = st.text_input("ইউটিউব ভিডিওর লিঙ্ক দিন:")

if st.button("ভিডিও তৈরি করো"):
    if url:
        try:
            with st.spinner("ইউটিউবের সিকিউরিটি পার করছি... একটু অপেক্ষা করুন।"):
                ydl_opts = {
                    'format': 'best[ext=mp4]',
                    'outtmpl': 'downloaded_video.mp4',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                st.video('downloaded_video.mp4')
                with open('downloaded_video.mp4', "rb") as f:
                    st.download_button("গ্যালারিতে সেভ করুন", f, file_name="video.mp4")
                st.success("সফল হয়েছে!")
        except Exception as e:
            st.error(f"দুঃখিত, ইউটিউব এখনও ব্লক করছে। এরর: {e}")
            
