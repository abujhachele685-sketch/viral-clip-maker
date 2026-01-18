import streamlit as st
from pytubefix import YouTube
import os

st.set_page_config(page_title="AI Viral Clip Maker Pro", page_icon="🎬")
st.title("🎬 AI Viral Clip Maker Pro")
st.write("YouTube লিঙ্ক দিয়ে প্রফেশনাল ক্লিপ তৈরি করুন।")

url = st.text_input("YouTube ভিডিওর লিঙ্ক এখানে দিন:")

if st.button("জাদুর মতো ক্লিপ তৈরি করো"):
    if url:
        try:
            with st.spinner("ভিডিও প্রসেস হচ্ছে... অনুগ্রহ করে অপেক্ষা করুন।"):
                yt = YouTube(url)
                video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                out_file = video.download()
                
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp4'
                os.rename(out_file, new_file)
                
                st.video(new_file)
                with open(new_file, "rb") as f:
                    st.download_button("ভিডিওটি গ্যালারিতে সেভ করুন", f, file_name="viral_clip.mp4")
                st.success("সফলভাবে ক্লিপ তৈরি হয়েছে!")
        except Exception as e:
            st.error(f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")
    else:
        st.warning("দয়া করে একটি সঠিক লিঙ্ক দিন।")
        
