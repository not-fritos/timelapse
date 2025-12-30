import subprocess
import glob
import os

def extract_frames():
    # Find all .mp4 files (case-insensitive)
    video_files = glob.glob("*.mp4") + glob.glob("*.MP4")
    
    if not video_files:
        print("No .mp4 files found in the current directory.")
        return

    for video in video_files:
        # Create a unique output folder for each video to prevent overwriting
        folder_name = f"frames_{os.path.splitext(video)[0]}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        output_pattern = os.path.join(folder_name, "out%d.png")
        
        print(f"Processing: {video}...")
        
        # Construct the FFmpeg command
        command = [
            'ffmpeg',
            '-i', video,
            '-vf', 'fps=1/5',
            output_pattern
        ]
        
        # Execute the command
        try:
            subprocess.run(command, check=True)
            print(f"Finished: {video} -> saved in {folder_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error processing {video}: {e}")

if __name__ == "__main__":
    extract_frames()
