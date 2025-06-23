import cv2
import os
from glob import glob
import subprocess

# Path to the folder containing images
image_folder = '/home/ubuntu/Desktop/results/VisDrone2019-SOT/uav0000099_02520_s'
output_video = 'output_video.mp4'
fps = 24  # Frames per second

# Get list of image files and sort them (e.g., 0001.jpg, 0002.jpg, ...)
image_files = sorted(glob(os.path.join(image_folder, '*.jpg')))

# Check if images are found
if not image_files:
    raise FileNotFoundError("No images found in the folder.")

# Read the first image to get dimensions
frame = cv2.imread(image_files[0])
height, width, _ = frame.shape

# Define video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For .mp4 file
video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

# Write each image to the video
for file in image_files:
    img = cv2.imread(file)
    img = cv2.resize(img, (width, height))  # Ensure all images have same size
    video_writer.write(img)

video_writer.release()
print(f"Video saved to {output_video}")

whatsapp_video = 'whatsapp_ready.mp4'

# --- Step 4: Use FFmpeg to convert to WhatsApp-friendly MP4 with silent audio ---
ffmpeg_cmd = [
    'ffmpeg', '-y',
    '-i', output_video,
    '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
    '-shortest',
    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
    '-c:v', 'libx264',
    '-profile:v', 'main',
    '-level', '3.1',
    '-pix_fmt', 'yuv420p',
    '-c:a', 'aac',
    '-b:a', '128k',
    '-movflags', '+faststart',
    whatsapp_video
]

subprocess.run(ffmpeg_cmd, check=True)
os.remove(output_video)

print(f"\n✅ Done! WhatsApp-compatible video saved as: {whatsapp_video}")