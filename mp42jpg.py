import argparse
import cv2
import random
from glob import glob as glob

def extract_single_frame(video_path, output_image_path, frame_number=None):
    """
    Extracts a single frame from a video and saves it as a JPG image.

    Args:
        video_path (str): The path to the input MP4 video file.
        output_image_path (str): The path where the output JPG image will be saved.
        frame_number (int, optional): The specific frame number to extract. 
                                      If None, a random frame will be extracted.
    """
    vidcap = cv2.VideoCapture(video_path)

    if not vidcap.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return

    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames == 0:
        print(f"Error: Video file '{video_path}' contains no frames.")
        vidcap.release()
        return

    if frame_number is None:
        # Extract a random frame
        #frame_to_extract = random.randint(0, total_frames - 1)
        frame_to_extract = 0
    else:
        # Extract a specific frame
        if 0 <= frame_number < total_frames:
            frame_to_extract = frame_number
        else:
            print(f"Warning: Frame number {frame_number} is out of bounds (0 to {total_frames - 1}). Extracting a random frame instead.")
            frame_to_extract = random.randint(0, total_frames - 1)

    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_to_extract)
    success, image = vidcap.read()

    if success:
        cv2.imwrite(output_image_path, image)
        print(f"Successfully extracted frame {frame_to_extract} and saved as '{output_image_path}'")
    else:
        print(f"Error: Could not read frame {frame_to_extract} from '{video_path}'")

    vidcap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converts HEIC/HEIF images to JPG format.",
        usage="%(prog)s [options] <heic_directory>",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("input_dir", type=str, help="Path to the directory containing HEIC images.")

    args = parser.parse_args()

    input_path = args.input_dir
    paths = glob(f"{input_path}/*.mp4") + glob(f"{input_path}/*.MP4")
    for path in paths:
        input_path = path
        #output_path = os.path.join(os.path.dirname(path), f"{os.path.basename(path).split(".")
        basename = path.split(".")[0]
        output_path = f"{basename}.jpg"

        print(f"converting {path}")
        extract_single_frame(input_path, output_path)

