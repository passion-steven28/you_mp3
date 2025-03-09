import os
from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse
from .forms import YouTubeURLForm
from .utils import download_video, video_to_mp3

def home(request):
    if request.method == 'POST':
        form = YouTubeURLForm(request.POST)
        if form.is_valid():
            try:
                url = form.cleaned_data['url']
                output_directory = os.path.join(settings.MEDIA_ROOT, 'downloads')
                os.makedirs(output_directory, exist_ok=True)

                video_path, video_title = download_video(url, output_directory)
                mp3_path = os.path.join(output_directory, f"{video_title}.mp3")
                video_to_mp3(video_path, mp3_path)

                # Clean up video file
                os.remove(video_path)

                return FileResponse(
                    open(mp3_path, 'rb'),
                    as_attachment=True,
                    filename=f"{video_title}.mp3"
                )
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = YouTubeURLForm()

    return render(request, 'converter/home.html', {'form': form})