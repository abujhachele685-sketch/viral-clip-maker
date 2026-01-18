import streamlit as st
import google.generativeai as genai
import yt_dlp
import os
from moviepy.editor import VideoFileClip

# আপনার দেওয়া API Key
genai.configure(api_key="AIzaSyCtSq9O0903w-GdJeQHHBqD2fTQ088QhCk")

st.set_page_config(page_title="AI Viral Clip Maker", page_icon="🔥")
st.title("🔥 AI Viral Clip Maker (Hiclip Style)")
st.write("বড় ভিডিও থেকে ১ মিনিটের ভাইরাল ক্লিপ, টাইটেল ও ফর্মুলা তৈরি করুন।")

url = st.text_input("YouTube ভিডিওর লিঙ্ক দিন:")

if st.button("ভাইরাল ক্লিপ ও ফর্মুলা তৈরি করো"):
    if url:
        try:
            with st.spinner("AI ভিডিও বিশ্লেষণ করছে... (ইউটিউব বাধা এড়ানোর চেষ্টা চলছে)"):
                # ১. ইউটিউব ভিডিও ডাউনলোড (আপডেটেড সেটিংস)
                ydl_opts = {
                    'format': 'best[ext=mp4]',
                    'outtmpl': 'main_video.mp4',
                    'noplaylist': True,
                    'quiet': True,
                    'no_warnings': True,
                    # নিচের এই লাইনটি ৪0৩ এরর এড়াতে সাহায্য করবে
                    'referer': 'https://www.youtube.com/',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # ২. Gemini AI বিশ্লেষণ
                video_file = genai.upload_file(path="main_video.mp4")
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                prompt = """এই ভিডিওটি বিশ্লেষণ করো। ১টি ভাইরাল অংশ খুঁজে বের করো যা ১ মিনিটের কম। 
                আমাকে ভাইরাল টাইটেল এবং কেন এটি ভাইরাল হবে (ফর্মুলা) জানাও।"""
                
                response = model.generate_content([prompt, video_file])
                
                # ৩. ভিডিও ক্লিপ কাটা
                full_video = VideoFileClip("main_video.mp4")
                clip_duration = min(59, full_video.duration) # ১ মিনিটের কম
                clip = full_video.subclip(0, clip_duration)
                clip.write_videofile("viral_short.mp4", codec="libx264")
                
                # ৪. ফলাফল দেখানো
                st.success("কাজ সম্পন্ন হয়েছে!")
                st.subheader("🚀 AI বিশ্লেষণ:")
                st.info(response.text)
                st.video("viral_short.mp4")
                
                with open("viral_short.mp4", "rb") as f:
                    st.download_button("গ্যালারিতে সেভ করুন", f, file_name="viral_clip.mp4")
                
                full_video.close()
                os.remove("main_video.mp4")

        except Exception as e:
            st.error(f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")
                
