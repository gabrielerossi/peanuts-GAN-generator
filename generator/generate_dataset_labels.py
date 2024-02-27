import json
import argparse
import os
import sys


def generate_labels(main_dir):
    data_dir = main_dir

    image_paths = []
    for root, _, files in os.walk(data_dir):
        for filename in files:
            if filename.endswith(".png"):
                image_paths.append(os.path.join(root, filename))

    labels = []

    for image_path in image_paths:
        directory_name = os.path.dirname(image_path)

        relative_dir_name = directory_name.replace(data_dir + "/", "")

        file_name = image_path.replace(directory_name + "/", "")

        if relative_dir_name == "snoopy":
            label = [os.path.join(relative_dir_name, file_name), 1]
        else:
            label = [os.path.join(relative_dir_name, file_name), 0]

        labels.append(label)

    with open(os.path.join(main_dir, "dataset.json"), "w") as f:
        json.dump({"labels": labels}, f)


def create_arg_parser():
    parser = argparse.ArgumentParser(description="Description of your app.")
    parser.add_argument("dir", help="Path to the directory with images.")
    return parser


if __name__ == "__main__":
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])

    if not os.path.exists(parsed_args.dir):
        print("Directory", parsed_args.dir, "doesn't exist")
        exit(1)

    generate_labels(parsed_args.dir)
