from flask import Flask, render_template, json, request, redirect, session, jsonify
from flask_cors import CORS
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import time
import json
import re
import base64

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

start_time = time.time()
print("Start training, Runtime:", time.time() - start_time)

np_save_object = np.load("sift_db.np.npy", allow_pickle=True)
flann = cv.FlannBasedMatcher()
print("Adding objects", flush=True)
for obj in np_save_object:
    flann.add([obj])
print("Train", flush=True)
flann.train()

sift = cv.SIFT_create()

print("Finished training, Runtime:", time.time() - start_time)

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

def parse_image_function(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

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
    
    return names   
    
app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/parse_image', methods=['POST'])
def parse_image():
    r = request.json
    nparr = np.fromstring(base64.b64decode(r['image']), np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    
    get_names = parse_image_function(img)
    return jsonify(get_names)

app.run()
