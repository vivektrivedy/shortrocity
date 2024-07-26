from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from moviepy.audio.fx.all import volumex

def add_music(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    #get length of video and trim audio
    length = video.duration
    audio = audio.set_duration(length)

    #reduce volume of audio
    audio = volumex(audio, 0.13)

    #overlay moviepy audio and set it to video
    new_audioclip = CompositeAudioClip([video.audio, audio])
    video.audio = new_audioclip

    #write new video
    video.write_videofile(output_path)
