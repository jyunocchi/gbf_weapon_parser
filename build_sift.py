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

weapon_id_to_sift = {}

sift = cv.xfeatures2d.SIFT_create()
for get_id, _ in weapon_id_pair:
    img = cv.imread("weapon_images/%s.jpg" % get_id)
    gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    
    a, b = sift.detectAndCompute(img,None)
    weapon_id_to_sift[get_id] = (a, b)
    
np_save_object = []
for get_id, _ in weapon_id_pair:
    np_save_object.append(weapon_id_to_sift[get_id][1])
np.save("sift_db.np", np.array(np_save_object, dtype=object))
