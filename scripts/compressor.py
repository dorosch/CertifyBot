"""
Compress all images used in the project.

To use, specify a path to the images:
    $ python3 scripts/compressor.py images/
"""

import argparse
import pathlib
import logging

from PIL import Image


def compress(path: pathlib.Path):
    image = Image.open(path)
    image.save(path, quality=20, optimize=True)


def main():
    parser = argparse.ArgumentParser(description="Compress images size")
    parser.add_argument(
        "--path",
        type=pathlib.Path,
        required=False,
        help="Path to the images",
        default=pathlib.Path(__file__).parent.parent.resolve() / "images"
    )
    args = parser.parse_args()
    path = args.path

    if not path.is_dir():
        return logging.error(f"Directory path '{path.absolute()}' doesn't exist")

    for image in path.rglob('*'):
        if image.is_dir():
            continue

        compress(image)


if __name__ == "__main__":
    main()
