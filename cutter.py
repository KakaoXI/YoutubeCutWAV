import os
import sys
from pydub import AudioSegment
from moviepy.editor import *

def download_youtube_video(url):
    try:
        video = YouTube(url)
        return video
    except Exception as e:
        print(f"Errore durante il download del video da YouTube: {e}")
        sys.exit(1)

def convert_video_to_wav(video_path, start_time, end_time):
    video_clip = VideoFileClip(video_path).subclip(start_time, end_time)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile("temp_audio.mp3")
    audio = AudioSegment.from_mp3("temp_audio.mp3")
    audio.export("output.wav", format="wav")
    os.remove("temp_audio.mp3")

if __name__ == "__main__":
    try:
        from pytube import YouTube
    except ImportError:
        print("Assicurati di aver installato pytube. Puoi farlo con 'pip install pytube'")
        sys.exit(1)

    youtube_url = input("Inserisci il link del video di YouTube: ")
    duration = input("Inserisci la durata del video (in secondi): ")
    end_time = input("Inserisci il tempo di fine (in secondi): ")

    video = download_youtube_video(youtube_url)
    video_path = video.streams.get_highest_resolution().download(filename="temp_video")

    try:
        duration = float(duration)
        end_time = float(end_time)
    except ValueError:
        print("Inserisci valori numerici validi per la durata e la fine del video.")
        sys.exit(1)

    if duration >= end_time:
        print("Il tempo di fine deve essere maggiore della durata.")
        sys.exit(1)

    convert_video_to_wav(video_path, duration, end_time)

    print("Conversione completata. Il file audio WAV è stato salvato come 'output.wav'")
