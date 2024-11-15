# GBF Weapon Parser

A parser that takes an image of a Granblue Fantasy (https://game.granbluefantasy.jp/) weapon grid as an input and returns the wiki (https://gbf.wiki/) format.

## Requirements

To run the python script (main.py) the following libraries are needed:
- numpy
- opencv
- matplotlib
- PIL
- tkinter
- tkinterdnd2

## Running the program

Either run by python script (python main.py) if you have all the prerequisites or the PyInstaller precompiled binary for windows provided in releases (main.exe).
TIPS: Not recommended to run exes found in the internet, you can run with [Windows Sandbox](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-overview) but will be more troublesome to move the images 

The following files are needed in the same directory. They are included in the release zip.
- icon.jpg (Yes this is needed, yes you can switch to any image you want, but why would you want that?)
- data.json (Mostly to get a pair of Weapon ID and name, from wiki cargotables)
- sift_db_np.npy (A precomputed SIFT database from the weapon images in the wiki)

If everything is running properly you should get a GUI like this after ~10s:

![alt text](https://github.com/jyunocchi/gbf_weapon_parser/blob/main/readme_img/main.jpg?raw=true)

Just drag and drop your image and you'll get your weapon grid!

![alt text](https://github.com/jyunocchi/gbf_weapon_parser/blob/main/readme_img/main2.jpg?raw=true)

## Notes

This repo uses traditional image matching by splitting the image into each weapon image and performing k-nearest neighbor to the precomputed database. Inaccuracy is expected.

## To-do

- More testing
- Get Taisai Spirit Bow (https://gbf.wiki/Taisai_Spirit_Bow) working. There may be other problematic images.
- Extra weapon slots
- Automated update script for data.json (cargotables query with python requests hasn't been working, so data.json is manually curated)
- Automated update of SIFT database once the previous point is done
- Better GUI (right now it's barebones GUI)
- Summon / character parser for full party?

## Other scripts

- build_sift.py

Opens data.json then opens all images in weapon_images/ID.jpg to build them into a SIFT database.
The SIFT database is then saved as sift_db_np.npy
