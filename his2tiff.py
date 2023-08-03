import argparse
from pathlib import Path
from tifffile import imwrite
from tqdm import tqdm
from HIS import HISReader


def main():
    parser = argparse.ArgumentParser(
        prog="his2tiff", description="convert HIS file to tiff image files"
    )
    parser.add_argument("input_file", help="HIS file path", type=str, action="store")
    parser.add_argument(
        "-o", "--output", help="output directory", type=str, action="store", default="."
    )
    args = parser.parse_args()
    inputfile = Path(args.input_file)
    outputdir = Path(args.output)
    outputdir.mkdir(exist_ok=True, parents=True)

    reader = HISReader(inputfile)
    nums = len(reader)
    digits = len(str(nums))
    comment = reader.comment.decode()
    for i, image in enumerate(tqdm(reader)):
        filename = outputdir / f"{inputfile.stem}{i:0{digits}}.tiff"
        imwrite(filename, image, metadata={"comment": comment}, software="his2tiff.py")


if __name__ == "__main__":
    main()
