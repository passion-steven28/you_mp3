import os
from pytube import YouTube
from pydub import AudioSegment
from django import forms


def download_video(url: str, output_directory: str) -> tuple[str, str]:
    """
    Downloads a YouTube video audio and returns the file path and title
    """
    try:
        # Add use_oauth=True and allow_oauth_cache=True for better access
        yt = YouTube(
            url,
            use_oauth=True,
            allow_oauth_cache=True
        )
        
        # Get the highest quality audio stream
        stream = yt.streams.filter(
            only_audio=True,
            file_extension='mp4'
        ).order_by('abr').desc().first()
        
        if not stream:
            raise Exception("No audio stream available")
            
        # Generate safe filename
        safe_title = "".join(x for x in yt.title if x.isalnum() or x in (' ', '-', '_')).rstrip()
        temp_file = os.path.join(output_directory, f"temp_{safe_title}.mp4")
        
        # Download the stream
        stream.download(output_path=output_directory, filename=f"temp_{safe_title}.mp4")
        return temp_file, safe_title
        
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")


def video_to_mp3(video_path: str, mp3_path: str) -> None:
    """
    Converts audio file to MP3 format
    """
    try:
        audio = AudioSegment.from_file(video_path)
        audio.export(mp3_path, format="mp3", bitrate="192k")
    except Exception as e:
        raise Exception(f"Error converting to MP3: {str(e)}")
    finally:
        # Clean up temp file
        if os.path.exists(video_path):
            os.remove(video_path)


class YouTubeURLForm(forms.Form):
    url = forms.URLField(
        label="YouTube URL", widget=forms.URLInput(attrs={"class": "form-control"})
    )
