import json
import os
import argparse
from config import source_dir_name, datasets_root
from video_motion_analyzer.motion_detector import MotionDetector


parser = argparse.ArgumentParser()

parser.add_argument("-v", "--video", help="path to video file", required=True)
parser.add_argument("-p", "--play", help="play video on background", type=bool, default=False)
parser.add_argument("-plt", "--plot", help="show plot statistics", type=bool, default=False)
parser.add_argument("-c", "--as_computer", help="allows to see the video as computer does", type=bool, default=False)
args = vars(parser.parse_args())


def main():
    video_path = args['video']
    video_file_path = os.path.join(datasets_root, source_dir_name, video_path)
    if not os.path.isfile(video_file_path):
        print("Please, provide correct video path")
        exit()

    video = MotionDetector(file_path=video_file_path, play_video=args["play"], as_computer=args["as_computer"])
    stats = video.prepare_motion_values_to_analyze(args["plot"])

if __name__ == "__main__":
    main()
