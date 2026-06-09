import om2bms_osz
import os
import json


if __name__ == "__main__":

    clear = lambda: os.system("cls")

    end = False
    curr_page = "main"

    # curr_opts = {
    #     "in_file": "input", 
    #     "set_default_out": open("./default_outdir.ini", "r").read().strip(),
    #     "hitsound": None, 
    #     "bg": True, 
    #     "video": True, 
    #     "offset": -235, 
    #     "judge": 2
    # }
    if not os.path.exists("./settings.json"):
        # incase someone for some reason deletes the settings file
        default_settings = {
            "in_file": "input", 
            "set_default_out": "output",
            "hitsound": None, 
            "bg": True, 
            "video": True, 
            "offset": -235, 
            "judge": 2
            }
        json.dump({"custom":default_settings, "default": default_settings}, open("./settings.json", "w"))

    curr_opts = json.load(open("./settings.json", "r"))["custom"]
    

    if not os.path.isdir(curr_opts["in_file"]):
        os.mkdir(curr_opts["in_file"])
        print(f"The missing input directory \"{curr_opts['in_file']}\" has been created. You can put your .osz files in there to convert.")
        input("Press ENTER to continue...")


    while not end:
        # updates options with whatever changes were made in previous iteration
        settings_file = json.load(open("./settings.json", "r"))
        settings_file["custom"] = curr_opts
        json.dump(settings_file, open("./settings.json", "w"))  

        # ugly format that shows the value of every setting at the beginning of each loop
        main_page_options = """Input Folder: {}\t\t Output Folder: {}\t\t\t Use Hitsounds: {}
Background Image: {}\t\t Default Map Offset: {}ms\t\t Judgement: {}
Background Video: {}""".format(curr_opts["in_file"], curr_opts["set_default_out"], "False" if curr_opts["hitsound"] is None else curr_opts["hitsound"],
                                                                                curr_opts["bg"], curr_opts["offset"], curr_opts["judge"], curr_opts["video"])


        clear()
        print("\n")
        print(main_page_options)
        print()

        # initial page display
        print("="*20 + "OPTIONS" + "="*20)
        if curr_page == "main":
            print("(1) Run Converter")
            print("(2) Edit Settings")
            print("(3) List Files To Convert")
            print("(4) Exit Program")
        elif curr_page == "settings":
            print("(1) Change Input Folder \t\t (2) Change Output Folder")
            print("(3) Toggle hitsounds \t\t\t (4) Toggle Convert Background Image")
            print("(5) Change Offset\t\t\t (6) Change Map Judgement")
            print("(7) Toggle Convert Background Video")
            print("\n(RESET): Reset these settings back to the system defaults")
            print("\n(0) Back to main page")
            




        print("")
        option = input("Choose option number: ").lower().strip()

        if curr_page == "main": # functionality for each option of main page
            if option == "1":
                # input_dir_scan = list(os.scandir(curr_opts["in_file"]))
                
                for file in os.scandir(curr_opts["in_file"]): # we loop across the path of every .osz file and convert them
                    if file.is_file() and file.path.endswith(".osz"):
                        curr_opts["in_file"] = file.path
                        om2bms_osz.convert(**curr_opts)

                print("\nConversion Complete\n")
                end = True
            elif option == "2":
                curr_page = "settings"
                clear()
            elif option == "3": # we just iterate over and display the filename of all .osz files in input file
                for file in os.scandir(curr_opts["in_file"]):
                    if file.is_file() and file.path.endswith(".osz"):
                        print(os.path.basename(file.path))
                    input("(Enter to clear)")
            elif option == "4":
                end = True
            else:
                input("ERROR: That option number does not exist!")
                
        elif curr_page == "settings": # functionality for each  option of settings page
            if option == "1":
                new_input = input("Enter new input folder: ").strip()
                if new_input:
                    curr_opts["in_file"] = new_input
                else:
                    input("ERROR: the input folder must be a none empty name.")
            elif option == "2":
                new_output = input("Enter new output folder: ").strip()
                if new_output:
                    curr_opts["set_default_out"] = new_output
                else:
                    input("ERROR: the output folder must be a none empty name.")
            elif option == "3":
                curr_opts["hitsound"] = not curr_opts["hitsound"]
            elif option == "4":
                curr_opts["bg"] = not curr_opts["bg"]
            elif option == "5":
                new_offset = input("Enter a new Offset (ms): ").strip()
                if all([num in map(str, range(10)) for num in (new_offset[1:] if new_offset[0] == "-" else new_offset)]):
                    curr_opts["offset"] = int(new_offset)
                else:
                    input("ERROR: you must enter a whole number for the offset!")
            elif option == "6":
                new_judgement = input("Enter a number for the map judgement: ").strip()
                if all([num in map(str, range(10)) for num in new_judgement]):
                    curr_opts["judge"] = int(new_judgement) 
                else:
                    input("ERROR: Judgement number must be a positive whole number!")
            elif option == "7":
                curr_opts["video"] = not curr_opts["video"]
            elif option == "reset":
                settings_file = json.load(open("./settings.json", "r"))
                curr_opts = settings_file["default"]
                # will update the "settings.json" on next iteration of the while loop
                
            elif option == "0":
                curr_page = "main"
            else:
                input("ERROR: That option number does not exist!")

