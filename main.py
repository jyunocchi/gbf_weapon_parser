import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import time
import json
from PIL import Image, ImageTk
import re

start_time = time.time()

f = open("data.json", encoding='utf-8')
get_json = json.loads(f.read())

weapon_id_pair = []
for arr in get_json['test']:
    for obj in arr['cargoquery']:
        if obj['title']['id'] != "1020001000":
            weapon_id_pair.append((obj['title']['id'], obj['title']['name']))

# specifically handle opus transcendence!
weapon_id_pair.append(('1040310600_02', 'Scythe of Repudiation (tc<4)'))
weapon_id_pair.append(('1040310600_03', 'Scythe of Repudiation (tc5)'))
weapon_id_pair.append(('1040310700_02', 'Scythe of Renunciation (tc<4)'))
weapon_id_pair.append(('1040310700_03', 'Scythe of Renunciation (tc5)'))

weapon_id_pair.append(('1040415000_02', 'Staff of Repudiation (tc<4)'))
weapon_id_pair.append(('1040415000_03', 'Staff of Repudiation (tc5)'))
weapon_id_pair.append(('1040415100_02', 'Staff of Renunciation (tc<4)'))
weapon_id_pair.append(('1040415100_03', 'Staff of Renunciation (tc5)'))

weapon_id_pair.append(('1040809400_02', 'Harp of Repudiation (tc<4)'))
weapon_id_pair.append(('1040809400_03', 'Harp of Repudiation (tc5)'))
weapon_id_pair.append(('1040809500_02', 'Harp of Renunciation (tc<4)'))
weapon_id_pair.append(('1040809500_03', 'Harp of Renunciation (tc5)'))

weapon_id_pair.append(('1040212500_02', 'Spear of Repudiation (tc<4)'))
weapon_id_pair.append(('1040212500_03', 'Spear of Repudiation (tc5)'))
weapon_id_pair.append(('1040212600_02', 'Spear of Renunciation (tc<4)'))
weapon_id_pair.append(('1040212600_03', 'Spear of Renunciation (tc5)'))

weapon_id_pair.append(('1040017000_02', 'Sword of Repudiation (tc<4)'))
weapon_id_pair.append(('1040017000_03', 'Sword of Repudiation (tc5)'))
weapon_id_pair.append(('1040017100_02', 'Sword of Renunciation (tc<4)'))
weapon_id_pair.append(('1040017100_03', 'Sword of Renunciation (tc5)'))

weapon_id_pair.append(('1040911000_02', 'Katana of Repudiation (tc<4)'))
weapon_id_pair.append(('1040911000_03', 'Katana of Repudiation (tc5)'))
weapon_id_pair.append(('1040911000_02', 'Katana of Renunciation (tc<4)'))
weapon_id_pair.append(('1040911000_03', 'Katana of Renunciation (tc5)'))

id_to_name = {}
for get_id, get_name in weapon_id_pair:
    id_to_name[get_id] = get_name

print("Start training, Runtime:", time.time() - start_time)

np_save_object = np.load("sift_db.np.npy", allow_pickle=True)
flann = cv.FlannBasedMatcher()

for obj in np_save_object:
    flann.add([obj])

flann.train()

print("Finished training, Runtime:", time.time() - start_time)

sift = cv.SIFT_create()

def get_closest_weapon(weapon):
    a, b = sift.detectAndCompute(weapon,None)
    matches = flann.knnMatch(b, k=2)
    
    match_ids = {}
    for m, n in matches:
        idx = m.imgIdx
        if idx not in match_ids:
            match_ids[idx] = []

        match_ids[idx].append(m.distance)
    
    
    matches = []
    for key in match_ids:
        current_score = -sum(match_ids[key]) / len(match_ids[key])
        matches.append((len(match_ids[key]), current_score, weapon_id_pair[key][0]))
    matches.sort(reverse=True)

    return matches[0][2]

def parse_image(image_path):
    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    h, w = gray.shape
    mh_x = w // 4
    first_x = w // 4 + w // 10 + w // 5
    second_x = first_x + w // 5

    first_y = h // 3
    second_y = 2 * h // 3

    # mainhand is one quarters to the left
    mh = gray[0:h, 0:mh_x]
    grid = [mh]
    x_cutoffs = [mh_x, first_x, second_x, w]
    y_cutoffs = [0, first_y, second_y, h]

    for i in range(1, len(y_cutoffs)):
        for j in range(1, len(x_cutoffs)):
            weapon = gray[y_cutoffs[i-1]:y_cutoffs[i], x_cutoffs[j-1]:x_cutoffs[j]]
            h2, w2 = weapon.shape
            weapon = weapon[0:(2 * h2 // 3), :]
            grid.append(weapon)
    
    text_names = ["|mh="]
    for i in range(1, 10):
        text_names.append("|wp%d=" % i)
    
    names = []
    for i in range(len(grid)):
        weapon = grid[i]
        best_id_match = get_closest_weapon(weapon)
        names.append(text_names[i] + id_to_name[best_id_match])
        
    for name in names:
        print(name)
    
    textbox.delete(1.0, tk.END)
    textbox.insert(1.0, "\n".join(names))
    
    b,g,r = cv.split(img)
    img = cv.merge((r,g,b))
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))
    image_panel.configure(image=imgtk)
    image_panel.image = imgtk
    
    print("Runtime:", time.time() - start_time)

import tkinter as tk

from tkinterdnd2 import DND_FILES, TkinterDnD

root = TkinterDnD.Tk()  # notice - use this instead of tk.Tk()

lb = tk.Listbox(root)
lb.insert(1, "drag files here")
lb.pack()

textbox = tk.Text(root)
textbox.insert(1.0, "Put images in to get output here")
textbox.pack()

icon_image = cv.imread("icon.jpg")
resized_image = cv.resize(icon_image, (80, 80)) 
b,g,r = cv.split(resized_image)
resized_image = cv.merge((r,g,b))
imgtk = ImageTk.PhotoImage(image=Image.fromarray(resized_image))
image_panel = tk.Label(root, image=imgtk)
image_panel.pack()

# register the listbox as a drop target
lb.drop_target_register(DND_FILES)
lb.dnd_bind('<<Drop>>', lambda e: parse_image(e.data))

root.mainloop()
