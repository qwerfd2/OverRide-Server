import zipfile
import os
import json
import shutil

from argparse import ArgumentParser
from om2bms.exceptions import BMSMaxMeasuresException
from om2bms.extra_file_processing import size_bg_thumbnail, cut_save_preview_audio
from types import SimpleNamespace

import om2bms.om_to_bms
import multiprocessing

def convert(in_file: str, set_default_out: str = None, hitsound: bool = None, bg: bool = True, video: bool = True, foldername: str = None, offset: int = -235, judge: int = 2):

    args = SimpleNamespace(**{ # Allows simpler use of the paramaters
        "in_file": in_file, 
        "set_default_out": set_default_out,
        "hitsound": hitsound,
        "bg": bg,
        "video": video,
        "foldername": foldername,
        "offset": offset,
        "judge": judge
    })

    cwd = os.getcwd()

    cfg_file = os.path.join(cwd, 'settings.json')
    if not os.path.exists(cfg_file):
        default_settings = {
            "in_file": "input", 
            "set_default_out": "output",
            "hitsound": None, 
            "bg": True, 
            "video": True, 
            "offset": -235, 
            "judge": 2
            }
        json.dump({"custom":default_settings, "default": default_settings}, open(cfg_file, "w"))

    # I know this whole if statement is weird, but I don't want to risk breaking anything any more
    if args.set_default_out is not None and args.set_default_out:
        # modifies output dir in json settings
        settings_obj = json.load(open(cfg_file, "r"))
        settings_obj["custom"]["set_default_out"] = args.set_default_out.strip()
        json.dump(settings_obj, open(cfg_file, "w"))

        outdir = args.set_default_out.strip()
    else:
        outdir = json.load(open(cfg_file, "r"))["custom"]["set_default_out"]

    if args.in_file is None:
        exit(0)

    if args.foldername is None:
        foldername = os.path.basename(args.in_file)[:-4]
        out_foldername = foldername
    else:
        out_foldername = args.foldername
        
    unzip_dir = os.path.join(cwd, "unzip_dir")
    if not os.path.isdir(unzip_dir):
        os.makedirs(unzip_dir)
    try:
        if not os.path.isdir(unzip_dir):
            os.makedirs(unzip_dir)

        filename = os.path.basename(args.in_file)
        shutil.copy2(args.in_file, unzip_dir)

        osz_dir = os.path.join(unzip_dir, filename)

        base = os.path.splitext(osz_dir)[0]
        os.rename(osz_dir, base + ".zip")
        osz_file_dir = base + ".zip"

        print("Unzipping...")
        with zipfile.ZipFile(osz_file_dir, 'r') as zipf:
            zipf.extractall(unzip_dir)

        output_file_dir = os.path.join(outdir, out_foldername)
        print("Output directory is " + output_file_dir)

        if not os.path.isdir(output_file_dir):
            os.makedirs(output_file_dir)

        processes = []
        manager = multiprocessing.Manager()
        bg_list = manager.list()
        audio_list = manager.list()
        for file in os.listdir(unzip_dir):
            if file.endswith(".osu"):
                filedir = os.path.join(unzip_dir, file)
                p = multiprocessing.Process(target=start_convertion,
                                            args=(filedir, output_file_dir, file, args, bg_list, audio_list))
                processes.append(p)


        for p in processes:
            p.start()

        for p in processes:
            p.join()

        if args.bg:
            print("Converting BG...")
            convert_bg_list(bg_list)
        
        print("Snipping preview audio...")
        make_preview_audio(audio_list)

        # move files to output directory
        for f in os.listdir(unzip_dir):
            if not os.path.isdir(os.path.join(unzip_dir, f)):
                if not f.split(".")[-1] == "zip" and not f.split(".")[-1] == "osu":
                    full_path = os.path.join(unzip_dir, f)
                    try:
                        shutil.copy2(full_path, output_file_dir)
                    except PermissionError as e:
                        print(e)
                        continue

        print("Done")
        # exit(0)
    except Exception as e:
        print(e)
        exit(1)
    finally:
        shutil.rmtree(unzip_dir)

def start_convertion(filedir_, output_file_dir_, file_, args, bg_list_, audio_list_):
    """
    Returns bg filename
    """
    try:
        om2bms.om_to_bms.OsuManiaToBMSParser._convertion_options = {
            "HITSOUND": None if args.hitsound == False else args.hitsound,
            "BG": args.bg,
            "VIDEO": args.video,
            "OFFSET": args.offset,
            "JUDGE": args.judge
        }
        
        converted_file = om2bms.om_to_bms.OsuManiaToBMSParser(filedir_, output_file_dir_, file_)
        if not converted_file.failed:
            if args.bg:
                bg_list_.append((converted_file.get_bg(), converted_file.beatmap.creator, converted_file.beatmap.beatmap_id))
            
            audio_list_.append((converted_file.get_audio_path(), converted_file.beatmap.preview_time, converted_file.beatmap.timing_points))
        

    except BMSMaxMeasuresException as e:
        print(e)

def make_preview_audio(audio_list_) -> None:
    """
    Creates a second audio file that we will use in the om2bms preview section
    (From osu map, uses either PreviewTime + 20s, first kiai section + 20s, 40% song + 20s)
    """

    seen = []
    for audio_info in audio_list_:
        audio_path, map_preview_time, map_timing_poins = audio_info
        if audio_path is not None and audio_path not in seen:
            cut_save_preview_audio(audio_path, map_preview_time, map_timing_poins)
            seen.append(audio_path)

def convert_bg_list(bg_list_) -> None:
    """
    Converts all images in img_list
    """
    seen = []
    for bg_info in bg_list_:
        bg, creator, beatmapid = bg_info
        if bg is not None and bg not in seen:
            size_bg_thumbnail(bg, creator, beatmapid)
            seen.append(bg)


if __name__ == "__main__":

    parser = ArgumentParser(description='Convert all .osu osu!mania files in a .osz to BMS files',
                            add_help=True,
                            allow_abbrev=True)

    parser.add_argument('-i', '--in_file',
                        action='store',
                        default=None,
                        help='Path to .osz to be converted.',
                        type=str)

    parser.add_argument('-sdo', '--set_default_out',
                        action='store',
                        default=None,
                        help='Sets the default output directory',
                        type=str)

    parser.add_argument('-hs', '--hitsound',
                        action='store_false',
                        default=None,
                        help='Disables hitsounds.')

    parser.add_argument('-b', '--bg',
                        action='store_false',
                        default=True,
                        help='Disables background image conversion.')
    
    parser.add_argument("-v", "--video",
                        action="store_false",
                        default=True,
                        help="Disables video conversion.")

    parser.add_argument('-f', '--foldername',
                        action='store',
                        default=None,
                        help='Directory name to store output files in output path. '
                             'Default value is the .osz filename')

    parser.add_argument('-o', '--offset',
                        default=-235,
                        type=int,
                        help="Adjusts music start time by [offset] ms.")

    parser.add_argument('-j', '--judge',
                        default=2,
                        type=int,
                        help="Judge difficulty. Defaults to EASY. "
                        "(3: EASY), (2: NORMAL), (1: HARD), (0: VERY HARD)")

    args = parser.parse_args()

    convert(**vars(args)) # because this function takes actual arguments instead of kwargs