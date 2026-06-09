from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageFont, ImageDraw
import os
from pydub import AudioSegment
from om2bms.data_structures import OsuTimingPoint

def appratio(t: int,b: int, val: float) -> int:
    """
    calculates a fixed ratio with t and b to then convert val according to that ratio.
    """
    return int((t/b)*val)

def cut_save_preview_audio(path_to_audio: str, preview_time: int, timing_points: list[OsuTimingPoint]) -> None:
    """
    Retrives a segment of an audio file and saves as preview_{filename}.mp3
    """
    
    filename = os.path.basename(path_to_audio)
    extention = filename.split(".")[-1]
    file_dir = os.path.dirname(path_to_audio)
    audio = AudioSegment.from_file(path_to_audio, format=extention)
    segment_length = 20000 # in milliseconds
    interval = [0,0]

    if preview_time >= 0: # if there was already a preview starting point defined in the osu map
        preview_time_end = preview_time + segment_length

        if len(audio) < preview_time_end:
            interval = [preview_time, len(audio)]
        else:
            interval = [preview_time, preview_time_end]

    elif timing_points != [] and any([tp.kiai_mode for tp in timing_points]): # if no defined preview point, take first kiai section
        i = 0
        while not timing_points[i].kiai_mode:
            i += 1

        start = timing_points[i].time
        end = start + segment_length

        if end > len(audio):
            end = len(audio)

        interval = [start, end]

    else: # if neither of the above, take default preview point that starts at 40% of the song
        start = int(len(audio)*0.4) 
        end = len(audio) if (start+segment_length) > len(audio) else start + segment_length
        interval = [start, end]

    preview_audio = audio[interval[0]:interval[1]] 
    new_filename = "preview_"+filename

    preview_audio.export(os.path.join(file_dir, new_filename), format=extention)


def size_bg_thumbnail(path_to_image: str, creator: str, beatmapid: str, thumbnail_size = (1000, 750)) -> None:
    """
    Resizes image to 700x700. Add black borders if image is widescreen.
    """
    
    source_image = Image.open(path_to_image).convert("RGB")
    background = source_image
    (sw, sh) = source_image.size
    thumbnail_w, thumbnail_h = thumbnail_size

    thumbnail_aspect = round(thumbnail_w/thumbnail_h, 3)
    source_aspect = round(sw/sh, 3)
    # print(thumbnail_aspect, source_aspect)

    if thumbnail_aspect == source_aspect or source_aspect < 1.333: 
        # if it's already the desired aspect, we'll only resize it and do no more processing on it.
        background.thumbnail((thumbnail_w, thumbnail_h))
        # background.show()
        background.save(path_to_image)
        background.close()
    else:
        # if it's not the desired aspect ratio, we fit it to an image with that aspect ratio (we also add text to the image in this case)

        zoomed_w, zoomed_h = round((sw/sh)*thumbnail_w), thumbnail_h
        # print(w, zoomed_w, h, zoomed_h)
        background.resize((zoomed_h, zoomed_w)) # resizes to h=700 aspect ratio
        background = ImageEnhance.Brightness(background).enhance(0.5) # dims image to 40% brightness
        background = background.filter(ImageFilter.GaussianBlur(6)) # blurs image
        background = ImageOps.fit(background, thumbnail_size) # fits/crops background image to the desired size

        source_image.thumbnail(thumbnail_size) # resizes source image
        paste_start_y = (thumbnail_h-source_image.height) // 2
        background.paste(source_image, (0, paste_start_y)) # places source image centered into the background

        curr_path = os.path.dirname(__file__) #because of some weird fucking path issue that the code is too dumb to understand (I spent an hour finding out this was the issue)
        font = ImageFont.truetype(os.path.join(curr_path, "allerregular.ttf"), appratio(22,700,thumbnail_w))
        draw = ImageDraw.Draw(background)

        # mapper
        text_offset = appratio(10,700, thumbnail_w)
        draw.text((text_offset ,paste_start_y-text_offset), "mapped by "+creator, (255,255,255), anchor="lb", font=font)
        # map uid
        draw.text((thumbnail_w-text_offset, paste_start_y + source_image.height + text_offset), "uid: /"+str(beatmapid), anchor="rt", font=font)
        


        # background.show()

        background.save(path_to_image)
        background.close()

# black_background_thumbnail("./lol.jpg", "Thor", "236", (700, 525))