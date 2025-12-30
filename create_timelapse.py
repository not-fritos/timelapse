import subprocess
import glob
import os

def combine_frames_to_video(output_filename="final_timelapse.mp4"):
    # Find all directories that start with 'frames_'
    folders = sorted([d for d in os.listdir('.') if os.path.isdir(d) and d.startswith('frames_')])
    
    if not folders:
        print("No frame folders found. Make sure to run the extraction script first.")
        return

    # Create a temporary file to list all images in order
    # This prevents 'glob' issues and handles large numbers of files across folders
    list_file = "images_to_process.txt"
    
    with open(list_file, "w") as f:
        for folder in folders:
            # Get all PNGs in the folder and sort them numerically
            images = sorted(glob.glob(os.path.join(folder, "*.png")), 
                            key=lambda x: int(os.path.basename(x).replace('out', '').replace('.png', '')))
            for img in images:
                # FFmpeg 'concat' demuxer requires 'file' prefix and absolute paths or safe relative paths
                f.write(f"file '{img}'\n")

    print(f"Combining frames from {len(folders)} folders...")

    # Construct the FFmpeg command using the concat demuxer
    # This is more robust than shell globs when dealing with multiple directories
    command = [
        'ffmpeg',
        '-r', '30',           # Input framerate
        '-f', 'concat',       # Use the concat demuxer
        '-safe', '0',         # Allow unsafe paths in the text file
        '-i', list_file,
        '-c:v', 'libx264',    # H.264 codec
        '-pix_fmt', 'yuv420p',# High compatibility pixel format
        '-crf', '23',         # High quality (lower is better, 18-28 is standard)
        output_filename
    ]

    try:
        subprocess.run(command, check=True)
        print(f"\nSuccess! Video created: {output_filename}")
        # Clean up the temporary list file
        os.remove(list_file)
    except subprocess.CalledProcessError as e:
        print(f"Error during video encoding: {e}")

if __name__ == "__main__":
    combine_frames_to_video()
