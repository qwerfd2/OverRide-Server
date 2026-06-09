# o!m2bms

[Original Repo](https://github.com/mashimycota/om2bms)

Program that converts osu!mania maps to BMS maps. (**currently only supports 2k to 8k**)

Supports fully keysounded maps and bpm changes.

**If you come across any Errors, please report them in the issues!**

## Installation

Written on Python 3.6+.
You can download the required libraries by running:
```
pip install -r requirements.txt
```

Requires an instance of ffmpeg in your system PATH. Here's an [ffmpeg installtion tutorial](https://phoenixnap.com/kb/ffmpeg-windows) if you don't have it already. (To check it if works, type `ffmpeg` in your terminal, and it should not return an error)


Set the default output directory by running,

```
python om2bms_osz.py -sdo [OUTPUT DIRECTORY]
```

or go to `default_outdir.ini` and paste the path to a subdirectory in a BMS songfolder directory.

## Running
Run

```
python om2bms_osz.py -i sample_osz_file.osz
```

to convert all 2k-8k files in `sample_osz_file.osz` and output them to `[OUTPUT DIRECTORY]/sample_osz_file`

To convert individual .osu files run

```
python om2bms_osu.py -i sample_osu_file.osu
```

#### Batch Converting

Run
```
python commandUI.py
```
To access the Command Line User Interface that allows some settings customisation and batch conversion of `.osz` files that are in the input folder (not compatible with single `.osu` files for now) 

(I personally think always converting `.osz` files is best anyway)


### To view help, run

```
python om2bms_osz.py -h
```

```
python om2bms_osu.py -h
```

## Key Mapping
(note: I will make images for this section in the future | will also make the layouts customizable)


Lets define the columns like this = `|1|2|3|4|5|6|7|8|`.

If a column is used for the key count in question, it will have it's corresponding number inside it.

### 2k
`|1| | | |5| | | |` (so 1k + scratch with controller)

### 3k
`| | | |4|5|6| | |`

### 4k
`| | |3|4| |6|7| |`

### 5k
`| |2|3|4|5|6| | |`

### 6k
`|1|2|3|4|5|6| | |` (so 5k + scratch if controller)

## To-do List

- [ ] Slider Velocity
- [ ] Difficulty calculation when converting 
- [x] *Background Videos* **(Needs to find fix for offset)**
- [x] Persistent settings file for UI
- [x] Support other keycounts then just 7k and 8k **(Supports 2k - 8k)**
- [ ] Improved background image resize/processing when converting
- [x] Adapt to be used without command line, aka a general run function for the arguments (necessary for GUI and improving command line UI)
- [ ] Make GUI
- [ ] Drag-and-drop for GUI
- [ ] Change output file format from `.bms` to `.bmson` (will allow easier feature implementation). Not to be done for a while. Will require big rewrite.

## Notes

- Tested with LR2
- Does not currently support SV changes
- Uses first timing point to estimate the first measure
- Assumes timing points are always the start of a new measure
- If there are >1 hitsounds played in one note, only plays the hitsound with the highest bit

[.osu file documentation](https://osu.ppy.sh/help/wiki/osu!_File_Formats/Osu_(file_format)).

[BMS file documentation](https://hitkey.nekokan.dyndns.info/cmds.htm).

## License

This project is licensed under the GPLv3 license, refer to LICENSE for details.

