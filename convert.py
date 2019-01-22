from subprocess import call
import os
import argparse


"""
Uses for converting mkv format video to mp4
Flags
- f full path to source dir with mkv files
- t full path to dir for mp4 store
Example of usage
python convert.py -f /home/developer/python/common_datasets/sets/h264 -t /home/developer/python/common_datasets/sets/h264
"""


parser = argparse.ArgumentParser()

parser.add_argument("-f", "--from_dir", help="full path to source dir with mkv files", required=True)
parser.add_argument("-t", "--to_dir", help="full path to dir for mp4 store", required=True)

args = vars(parser.parse_args())


def convert(from_file_path, to_file_path):
    command = "ffmpeg -i %s.mkv -f matroska %s.mp4" % (from_file_path, to_file_path)
    call(command.split())

if __name__ == "__main__":
    from_dir = args["from_dir"]
    to_dir = args["to_dir"]
    for f in os.listdir(from_dir):
        print(os.path.join(from_dir, f))
        from_list = os.path.splitext(os.path.join(from_dir, f))
        from_path = from_list[0]

        if from_list[1] == '.mkv':
            convert(from_path, to_dir)
