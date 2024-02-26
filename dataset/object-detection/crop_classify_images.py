import os
import cv2
import argparse
import sys


def crop_images(txt_dir, image_dir, output_snoopy, output_charlie):
    total = len([name for name in os.listdir(txt_dir)])
    i = 1
    for filename in os.listdir(txt_dir):
        txt_path = os.path.join(txt_dir, filename)
        image_path = os.path.join(image_dir, filename.split(".")[0] + ".png")

        img = cv2.imread(image_path)

        with open(txt_path, "r") as f:
            for line in f:
                splitted_line = line.split()
                object_id = int(splitted_line[0])

                if object_id == 1:
                    output_dir = output_snoopy
                else:
                    output_dir = output_charlie

                os.makedirs(output_dir, exist_ok=True)

                xcenter, ycenter, w, h = map(float, splitted_line[1:])

                left = int((xcenter - (w / 2))* img.shape[1])
                top = int((ycenter - (h / 2))* img.shape[0])
                right = int(left + (w*img.shape[1]))
                bottom = int(top + (h*img.shape[0]))

                cropped_image = img[top:bottom, left:right]

                output_path = os.path.join(output_dir, filename.split(".")[0] + ".png")
                cv2.imwrite(output_path, cropped_image)
            print("image ", i ,"/", total, " ", txt_path)
            i += 1


def create_arg_parser():
    parser = argparse.ArgumentParser(description="Description of your app.")
    parser.add_argument("txtDir", help="Path to the directory with .txt file.")
    parser.add_argument(
        "imageDir", help="Path to the directory that contains input images."
    )
    parser.add_argument(
        "outputSnoopy",
        help="Path to the output directory that contains Snoopy cropped images.",
    )
    parser.add_argument(
        "outputCharlie",
        help="Path to the output directory that contains Charlie cropped images.",
    )
    return parser


def _create_directory(dir):
    os.makedirs(dir, exist_ok=True)


if __name__ == "__main__":
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])

    if not os.path.exists(parsed_args.txtDir):
        print("Directory", parsed_args.txtDir, "doesn't exist")
        exit(1)
    if not os.path.exists(parsed_args.imageDir):
        print("Directory", parsed_args.imageDir, "doesn't exist")
        exit(1)

    if not os.path.exists(parsed_args.outputSnoopy):
        _create_directory(parsed_args.outputSnoopy)
    if not os.path.exists(parsed_args.outputCharlie):
        _create_directory(parsed_args.outputCharlie)

    crop_images(
        parsed_args.txtDir,
        parsed_args.imageDir,
        parsed_args.outputSnoopy,
        parsed_args.outputCharlie,
    )
