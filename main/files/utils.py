
import ffmpeg
import os
from moviepy.editor import VideoFileClip
from speech_recognition import AudioFile, Recognizer
from srt import Subtitle as sub
import srt

def generate_video_thumbnail(video_path, time_point=5, thumbnail_size=(256, 144)):
    """
    Generates a thumbnail from a video at a specific time and size.

    Parameters:
        video_path (str): Path to the video file.
        time_point (int): Time in seconds to capture the thumbnail from (default: 5 seconds).
        thumbnail_size (tuple): Desired size of the thumbnail (width, height) in pixels (default: 256x144).

    Returns:
        thumbnail (PIL.Image): The generated thumbnail image.
    """

    # Load the video clip
    clip = VideoFileClip(video_path)

    # Capture a frame at the specified time_point
    frame = clip.get_frame(time_point)

    # Create a copy of the frame to avoid modifying the original frame
    frame_copy = frame.copy()

    # Resize the copied frame to the desired thumbnail size
    thumbnail = frame_copy.resize(thumbnail_size)

    # Convert the image to RGB format for PIL compatibility
    thumbnail = thumbnail.convert("RGB")

    # Return the thumbnail image
    return thumbnail

def generate_srt_subtitles(video_file, language="en", chunk_duration=5):
    """
    Generates SRT subtitles from a video file and returns a dictionary
    suitable for creating a Django Subtitle object.

    Args:
      video_file (str): Path to the video file.
      language (str): Language of the audio in the video (default: English).
      chunk_duration (int): Duration of each subtitle chunk in seconds (default: 5).

    Returns:
      subtitle_dict (dict): Dictionary containing subtitle data for a Django Subtitle object.
    """

    # Extract audio from the video
    clip = VideoFileClip(video_file)
    audio_file = f"{video_file}_temp.wav"
    clip.audio.write_audiofile(audio_file)

    # Transcribe the audio
    r = Recognizer()
    with AudioFile(audio_file) as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language=language)

    # Split the text into chunks based on the specified duration
    chunks = [text[i:i + chunk_duration] for i in range(0, len(text), chunk_duration)]

    # Generate timestamps based on video scene changes (simplified assumption)
    timestamps = [(i * chunk_duration, (i + 1) * chunk_duration) for i in range(len(chunks))]

    # Create subtitle objects and format subtitle data
    subtitle_entries = []
    for i, chunk in enumerate(chunks):
        start, end = timestamps[i]
        subtitle_entries.append(sub(index=i + 1, start=srt.timedelta(seconds=start), end=srt.timedelta(seconds=end), content=chunk))
    srt_string = srt.serialize(subtitle_entries)

    # Clean up temporary audio file
    os.remove(audio_file)

    return srt_string, language


def convert_and_save(input_file, resolution="720p"):
    """
    Converts a video file to a streamable format with a specific resolution and saves the information to the EncodedVideo model.

    Args:
        input_file (str): Path to the input video file.
        resolution (str): Target resolution for the video (e.g., "480p", "720p", "1080p").

    Returns:
        EncodedVideo: The saved EncodedVideo instance.
    """

    # Resolution mapping
    resolutions = {
        "240p": (426, 240),
        "360p": (640, 360),
        "480p": (854, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
    }

    # Check if the specified resolution is valid
    if resolution not in resolutions:
        raise ValueError(f"Invalid resolution. Supported resolutions: {', '.join(resolutions.keys())}")

    # Get the resolution tuple
    width, height = resolutions[resolution]

    # Generate output file name based on input file and resolution
    base_name, extension = os.path.splitext(os.path.basename(input_file))
    output_file = f"{base_name}_{resolution}{extension}"

    # Specify desired video and audio codecs and bitrates
    stream = ffmpeg.input(input_file).output(
        output_file,
        vcodec="libx264",
        acodec="aac",
        ar="44100",
        ac="2",
        vf=f"scale={width}:{height}",
        b="3000k",  # You can adjust this bitrate based on your requirements
        pix_fmt="yuv420p",
        strict="experimental",
    )

    # Run the conversion process
    stream.run(overwrite_output=True)

    print(f"{output_file} encoded")
    return output_file

