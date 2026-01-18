import streamlit as st
import yt_dlp
import os

# ওয়েবসাইটের শিরোনাম
st.set_page_config(page_title="AI Viral Clip Maker", page_icon="🎬")
st.title("🎬 AI Viral Clip Maker Pro")
st.markdown("YouTube লিংক দিয়ে প্রফেশনাল ক্লিপ তৈরি করুন।")

# ইনপুট বক্স
url = st.text_input("YouTube ভিডিওর লিঙ্ক এখানে দিন:")

if st.button("জাদুর মতো ক্লিপ তৈরি করো"):
    if url:
        with st.spinner("আপনার ভিডিওটি প্রসেস হচ্ছে... একটু অপেক্ষা করুন।"):
            try:
                # ভিডিও ডাউনলোড করার সেটিংস
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': 'downloaded_video.mp4',
                    'noplaylist': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                st.success("✅ ভিডিও তৈরি হয়েছে!")
                
                # ভিডিও প্লেয়ার দেখানো
                video_file = open('downloaded_video.mp4', 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes)
                
                # ডাউনলোড বাটন
                st.download_button(label="ভিডিওটি সেভ করুন", data=video_bytes, file_name="viral_clip.mp4", mime="video/mp4")
                
                # কাজ শেষ হলে ফাইলটি মুছে ফেলা যাতে সার্ভারে জায়গা বাঁচে
                video_file.close()
                os.remove("downloaded_video.mp4")
                
            except Exception as e:
                st.error(f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")
    else:
        st.warning("অনুগ্রহ করে একটি সঠিক ইউটিউব লিঙ্ক দিন।")
      
