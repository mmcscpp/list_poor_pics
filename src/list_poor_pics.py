import argparse
import os
import shutil
from collections.abc import Generator

from PIL import Image

from axes import Axes
from pic_checker import PicRatioChecker
from pic_checker import PicSizeChecker


POOR_PICS_FOLDER = "poor_pics"

# Änderung 2
class Settings:
    def __init__(self) -> None:
        self.move_flag = False
        self.verbose_flag = False
        # dimensions in pixels
        self.dim_1st_px = 900
        self.dim_2nd_px = 1200


# implemented as generator function
def get_pics(pic_path: str) -> Generator[tuple[str, Axes]]:
    """ yields a tuple: (file path, axes) """
    jpg_ext = ".jpg"

    for folder_name, _, file_names in os.walk(pic_path):
        # '_' is the placeholder for sub_folder_name
        # print(f"Verzeichnis: {folder_name}")

        # for sub_folder_name in sub_folder_names:
        #    print(f"Unterverzeichnis: {sub_folder_name}")

        for file_name in file_names:
            pic_complete_path = os.path.join(folder_name, file_name)         # fuegt automatisch den richtigen Separator hinzu
            if pic_complete_path.endswith(jpg_ext) and (POOR_PICS_FOLDER not in pic_complete_path):
                # print(f"Datei: {pic_complete_path}")
                pic = Image.open(pic_complete_path)
                pic_axes = Axes(pic.width, pic.height)
                pic.close()

                yield pic_complete_path, pic_axes


def move_poor_pic(pic_path: str, to_folder: str) -> bool:
    pic_file_name = os.path.basename(pic_path)
    # '_' is the placeholder for folder name

    poor_pic_path = os.path.join(to_folder, pic_file_name)
    if not os.path.exists(poor_pic_path):
        shutil.move(pic_path, poor_pic_path)
        return True
    return False


def main(pic_folder: str, settings: Settings) -> None:

    if not os.path.exists(pic_folder):
        print(f"Directory '{pic_folder}' does not exist!")
        exit()

    poor_pic_folder = os.path.join(pic_folder, POOR_PICS_FOLDER)
    if settings.move_flag:
        if not os.path.exists(poor_pic_folder):
            os.mkdir(poor_pic_folder)

    pic_size_checker = PicSizeChecker(Axes(settings.dim_1st_px - 2, settings.dim_2nd_px - 2))
    pic_ratio_checker = PicRatioChecker()

    num_files_moved = 0
    # setup generator for reading the file names in the passed folder
    pics_getter = get_pics(pic_folder)
    while True:
        # get next file name and its axes; next() with default argument if generator is empty
        pic_path, pic_axes = next(pics_getter, ("", Axes(0, 0)))
        if pic_path == "":
            break

        pic_file_name = os.path.basename(pic_path)
        info = f"{pic_file_name} ({pic_axes}) "

        too_small = pic_size_checker.check(pic_path, pic_axes)
        bad_ratio = pic_ratio_checker.check(pic_path, pic_axes)

        file_moved = False
        if too_small or bad_ratio:
            if too_small and bad_ratio:
                info += "--> too_small, bad_ration"
            elif too_small:
                info += "--> too_small"
            else:
                info += "--> bad_ratio"

            if settings.move_flag and not file_moved:
                file_moved = move_poor_pic(pic_path, poor_pic_folder)
                if file_moved:
                    num_files_moved += 1

        if settings.verbose_flag and info:
            print(f"{info}", end="")
            if file_moved:
                print(", file moved")
            else:
                print()

    print(f"{pic_size_checker.to_string()}")
    print(f"{pic_ratio_checker.to_string()}")
    if settings.move_flag:
        print(f"{num_files_moved} files move to subfolder {poor_pic_folder}.")

    print("good bye")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script to find and move pictures which are too small or with a bad width-to-height ratio"
    )
    parser.add_argument("-d", "--dimensions", type=str, help="dimensions in pixels, e.g. 1920x1080")
    parser.add_argument("-m", "--move", action="store_true", help=f"moves found (too small and bad ratio) pictures to sub-folder '{POOR_PICS_FOLDER}'")
    parser.add_argument("--verbose", action="store_true", help="enables some console outputs")
    parser.add_argument("folder", type=str, help="folder name containing the pictures")
    args = parser.parse_args()

    pic_path = args.folder
    settings = Settings()
    if args.dimensions:
        pos = args.dimensions.find("x")
        if pos != -1:
            settings.dim_1st_px = int(args.dimensions[:pos])
            pos += 1
            settings.dim_2nd_px = int(args.dimensions[pos:])

    if args.move:
        settings.move_flag = True
    settings.verbose_flag = args.verbose

    # pic_path = "D:\\Galerien\\Blumen\\"
    main(pic_path, settings)
