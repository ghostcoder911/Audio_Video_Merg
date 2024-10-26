from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import os

def format_bullet_points(points):
    """Format the bullet points with proper spacing"""
    return '\n\n'.join(f"• {point}" for point in points)

def replace_audio_and_add_text(video_path: str, audio_path: str, output_path: str, bullet_points: list):
    """
    Replace the audio of a video and add bullet points text at the left side for the last 10 seconds.
    Audio will be adjusted to match video length.
    
    Args:
        video_path (str): Path to the input video file
        audio_path (str): Path to the new audio file
        output_path (str): Path for the output video file
        bullet_points (list): List of strings for bullet points
    """
    try:
        # Load the video
        print("Loading video...")
        video_clip = VideoFileClip(video_path)
        video_duration = video_clip.duration
        
        # Load and adjust the audio to match video length
        print("Loading and adjusting audio...")
        new_audio = AudioFileClip(audio_path)
        if new_audio.duration != video_duration:
            if new_audio.duration > video_duration:
                # If audio is longer, cut it
                new_audio = new_audio.subclip(0, video_duration)
            else:
                # If audio is shorter, loop it
                repeats = int(video_duration / new_audio.duration) + 1
                new_audio = new_audio.loop(repeats)
                new_audio = new_audio.subclip(0, video_duration)
        
        # Set the new audio to the video clip
        video_with_new_audio = video_clip.set_audio(new_audio)
        
        # Calculate start time for text (10 seconds before the end)
        text_start_time = max(0, video_duration - 10)
        
        # Format bullet points with proper spacing
        formatted_text = format_bullet_points(bullet_points)
        
        # Create text clip with bullet points
        print("Creating text overlay...")
        text_clip = TextClip(
            formatted_text,
            fontsize=30,
            color='white',
            font='Arial',
            method='label',
            align='west',  # Left alignment
            stroke_color='black',  # Add black outline for better visibility
            stroke_width=2  # Thickness of the outline
        )
        
        # Position text on the left side with some padding
        # and make it appear for the last 10 seconds
        text_clip = text_clip.set_position((50, 'center'))  # 50 pixels from left
        text_clip = text_clip.set_start(text_start_time)
        text_clip = text_clip.set_duration(10)
        
        # Combine video with text overlay
        print("Combining video and text...")
        final_video = CompositeVideoClip([video_with_new_audio, text_clip])
        
        # Write the result to the output file
        print("Writing output file...")
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=video_clip.fps  # Use original video's fps
        )
        
        print(f"Successfully saved to: {output_path}")
        
        # Clean up
        video_clip.close()
        new_audio.close()
        final_video.close()
        text_clip.close()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e

if __name__ == "__main__":
    # Example bullet points
    bullet_points = [
        "First important point",
        "Second key message",
        "Third crucial information",
        "Final takeaway"
    ]
    
    # Replace audio and add text to the video
    replace_audio_and_add_text(
        video_path="input_video.mp4",
        audio_path="new_audio.mp3",
        output_path="output_video.mp4",
        bullet_points=bullet_points
    )
