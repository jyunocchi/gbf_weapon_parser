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

Either run by python script (python main.py) or the PyInstaller precompiled binary for windows (main.exe)
The following files are needed in the same directory. They are included in the release.
- icon.jpg (Yes this is needed, yes you can switch to any image you want)
- data.json (Mostly to get a pair of Weapon ID and name, from wiki cargotables)
- sift_db_np.npy (A precomputed SIFT database from the weapon images in the wiki)

## Notes

This repo uses traditional image matching by splitting the image into each weapon image and performing k-nearest neighbor to the precomputed database. Inaccuracy is expected.

## To-do

- More testing
- Get Taisai Spirit Bow (https://gbf.wiki/Taisai_Spirit_Bow) working
- Extra weapon slots
- Summon / character parser for full party?
