import streamlit as st
import os
import tempfile
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import numpy as np
from scipy.io import wavfile
import io

# Function to download video using pytube with OAuth
def download_video(url, output_path):
    try:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        stream.download(output_path=output_path)
        return yt.title, os.path.join(output_path, stream.default_filename)
    except Exception as e:
        st.error(f"Error downloading video: {e}")
        return None, None

# Function to identify viral moments (simple audio peak detection)
def identify_viral_moments(video_path, clip_duration=60):
    clip = VideoFileClip(video_path)
    duration = clip.duration
    audio = clip.audio
    
    # Export audio to temporary WAV for analysis
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
        audio.write_audiofile(temp_audio.name, verbose=False, logger=None)
        sample_rate, data = wavfile.read(temp_audio.name)
    
    # Calculate RMS energy
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)  # Convert to mono if stereo
    window_size = int(sample_rate * 1)  # 1-second windows
    rms = []
    for i in range(0, len(data) - window_size, window_size):
        rms.append(np.sqrt(np.mean(data[i:i+window_size]**2)))
    
    # Find peaks (top 10% energy moments)
    threshold = np.percentile(rms, 90)
    viral_times = [i * 1 for i, r in enumerate(rms) if r > threshold]
    
    # Group into 60-second clips around peaks
    clips = []
    for start in viral_times:
        end = min(start + clip_duration, duration)
        if end - start >= clip_duration:
            clips.append((start, end))
    
    # If no peaks, fall back to every 60 seconds
    if not clips:
        for start in range(0, int(duration), clip_duration):
            end = min(start + clip_duration, duration)
            if end - start >= clip_duration:
                clips.append((start, end))
    
    return clips

# Function to cut clips
def cut_clips(video_path, clips, output_dir):
    clip_files = []
    for i, (start, end) in enumerate(clips):
        video_clip = VideoFileClip(video_path).subclip(start, end)
        output_file = os.path.join(output_dir, f"viral_clip_{i+1}.mp4")
        video_clip.write_videofile(output_file, verbose=False, logger=None)
        clip_files.append(output_file)
    return clip_files

# Function to generate viral titles and descriptions
def generate_titles_descriptions(video_title, num_clips):
    titles = []
    descriptions = []
    for i in range(num_clips):
        title = f"🔥 VIRAL MOMENT: {video_title} - Epic Clip {i+1} 🔥"
        desc = f"Check out this insane viral moment from '{video_title}'! Watch the highlights and share with your friends. #Viral #YouTube #Highlights #EpicMoments"
        titles.append(title)
        descriptions.append(desc)
    return titles, descriptions

# Streamlit App
st.title("YouTube Viral Clipper")
st.markdown("Enter a YouTube URL to download, identify viral moments, cut into 60-second clips, and generate titles/descriptions.")

url = st.text_input("YouTube URL:")
if st.button("Process Video"):
    if url:
        with st.spinner("Downloading video..."):
            with tempfile.TemporaryDirectory() as temp_dir:
                video_title, video_path = download_video(url, temp_dir)
                if video_path:
                    st.success(f"Downloaded: {video_title}")
                    
                    with st.spinner("Identifying viral moments..."):
                        clips = identify_viral_moments(video_path)
                        st.info(f"Found {len(clips)} viral clips.")
                    
                    with st.spinner("Cutting clips..."):
                        clip_files = cut_clips(video_path, clips, temp_dir)
                    
                    titles, descriptions = generate_titles_descriptions(video_title, len(clips))
                    
                    st.header("Generated Clips and Metadata")
                    for i, clip_file in enumerate(clip_files):
                        st.subheader(f"Clip {i+1}")
                        st.video(clip_file)
                        st.write(f"**Title:** {titles[i]}")
                        st.write(f"**Description:** {descriptions[i]}")
                        with open(clip_file, "rb") as f:
                            st.download_button(
                                label=f"Download Clip {i+1}",
                                data=f,
                                file_name=f"viral_clip_{i+1}.mp4",
                                mime="video/mp4"
                            )
                else:
                    st.error("Failed to download video.")
    else:
        st.warning("Please enter a valid YouTube URL.")
