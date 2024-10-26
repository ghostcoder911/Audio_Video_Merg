from moviepy.editor import VideoFileClip, AudioFileClip

def replace_audio_in_video(video_path: str, audio_path: str, output_path: str):
    """
    Replace the audio of a video with a new audio track.

    Args:
        video_path (str): Path to the input video file.
        audio_path (str): Path to the new audio file.
        output_path (str): Path for the output video file with replaced audio.
    """
    try:
        # Load the video
        video_clip = VideoFileClip(video_path)
        
        # Load the new audio
        new_audio = AudioFileClip(audio_path)
        
        # Set the new audio to the video clip
        video_with_new_audio = video_clip.set_audio(new_audio)
        
        # Write the result to the output file
        video_with_new_audio.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        print(f"Output saved to: {output_path}")
        
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    # Example paths (update these with your actual file paths)
    input_video = "input_video.mp4"  # Path to the video file
    input_audio = "new_audio.mp3"    # Path to the audio file
    output_video = "output_video.mp4" # Path for the output video

    # Replace audio in the video
    replace_audio_in_video(input_video, input_audio, output_video)

