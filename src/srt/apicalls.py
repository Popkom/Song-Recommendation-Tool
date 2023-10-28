import requests
import json
from itertools import islice
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import random

app = Flask(__name__)
CORS(app)

API_KEY = "1b5e19b6420f8b125a4f68e3c840eaa3"
useragent = "LIoannou - UofG Song Recommendation Tool"
profile = {}
inputs = {}
tagdict = {}


@app.route("/api/data", methods=["POST"])
def receive_song():
    global inputs
    global profile
    data = request.json
    if data == "r":
        latest = list(inputs.keys())[-1]
        rating = inputs[latest][3]
        for i in range(3):
            profile[inputs[latest][i]] = profile[inputs[latest][i]] - int(rating)
        inputs.pop(latest)
        sortedprof = sorted(profile.items(), key=lambda x: x[1], reverse=True)
        profile = dict(sortedprof)
        return jsonify({"message": "Success"})
    if data == "c":
        inputs = {}
        profile = {}
        return jsonify({"message": "Success"})
    songdata = data.split("/")
    respandtrack = lastfm_get({"track": songdata[0], "artist": songdata[1]})
    tags = gettags(respandtrack[0])
    inputs[respandtrack[1] + " - " + respandtrack[2]] = tags.copy()
    inputs[respandtrack[1] + " - " + respandtrack[2]].append(songdata[2])
    updateprofile(tags, songdata[2])
    return jsonify({"message": respandtrack[1] + " - " + respandtrack[2]})


@app.route("/api/submit-songs", methods=["POST"])
def submit_songs():
    global profile
    data = get_data(profile)
    params = request.json.split("/")
    numofrecs = params[0]
    numfofsames = params[1]
    print(numofrecs)
    print(numfofsames)
    recs = calcscores(profile, data[0], data[1], int(numofrecs), int(numfofsames))
    recsasstring = ", ".join(recs)
    taglist = list(profile.keys())[0:3]
    topthree = " - ".join(taglist)
    profile = {}
    return jsonify(
        {
            "message": "Recommendations: "
            + recsasstring
            + "\n"
            + "Taste profile: "
            + topthree
        }
    )


def lastfm_get(payload):
    url = "https://ws.audioscrobbler.com/2.0"

    payload["api_key"] = API_KEY
    payload["format"] = "json"
    payload["method"] = "track.search"
    payload["autocorrect"] = "1"
    response = requests.get(url, params=payload)
    jsonresp = response.json()
    payload["track"] = jsonresp["results"]["trackmatches"]["track"][0]["name"]
    payload["artist"] = jsonresp["results"]["trackmatches"]["track"][0]["artist"]
    payload["method"] = "track.gettoptags"
    response = requests.get(url, params=payload)
    return [response, payload["track"], payload["artist"]]


# def update_inputs()


def gettags(resp):
    actual = resp.json()
    tagslist = actual["toptags"]["tag"]
    tags = []
    i = 0
    if len(tagslist) >= 3:
        while (len(tags) < 3) and (i < len(tagslist)):
            currenttag = tagslist[i]["name"]
            if (currenttag[0] != "-") and (currenttag != "MySpotigramBot"):
                tags.append(currenttag + "/" + str(tagslist[i]["count"]))
            i = i + 1
    else:
        for j in range(len(tagslist)):
            currenttag = tagslist[i]["name"]
            if (currenttag[0] != "-") and (currenttag != "MySpotigramBot"):
                tags.append(currenttag + "/" + (tagslist[i]["count"]))
    return tags


def updateprofile(tags, rating):
    global profile
    for i in range(len(tags)):
        tagdata = tags[i].split("/")
        if tagdata[0] in profile:
            profile[tagdata[0]] = profile[tagdata[0]] + (
                float(rating) * float(tagdata[1])
            )
        else:
            profile[tagdata[0]] = float(rating) * float(tagdata[1])
    sortedprof = sorted(profile.items(), key=lambda x: x[1], reverse=True)
    profile = dict(sortedprof)


def get_data(profile):
    print(profile)
    payload = {}
    url = "https://ws.audioscrobbler.com/2.0"
    payload["api_key"] = API_KEY
    payload["format"] = "json"
    payload["method"] = "tag.gettoptracks"
    tracks = {}
    artists = []
    for i in range(3):
        payload["tag"] = list(profile.keys())[i]
        payload["page"] = 1
        for j in range(4):
            response = requests.get(url, params=payload)
            fullresp = response.json()["tracks"]["track"]
            for k in range(len(fullresp)):
                tracks[fullresp[k]["name"] + " - " + fullresp[k]["artist"]["name"]] = [
                    fullresp[k]["artist"]["name"],
                    payload["tag"],
                ]
            payload["page"] = str(j + 1)
            time.sleep(0.5)
    payload["method"] = "tag.gettopartists"
    payload["page"] = "1"
    for i in range(3):
        payload["tag"] = list(profile.keys())[i]
        response = requests.get(url, params=payload)
        fullresp = response.json()["topartists"]["artist"]
        for j in range(len(fullresp)):
            artists.append(fullresp[j]["name"])
    for item in tracks.items():
        for i in range(len(artists)):
            if item[1][0] == artists[i]:
                if i < 50:
                    tracks[item[0]][1] = list(profile.keys())[0]
                elif i < 100:
                    tracks[item[0]][1] = list(profile.keys())[1]
                else:
                    tracks[item[0]][1] = list(profile.keys())[2]
    return [tracks, artists]


def calcscores(profile, tracks, artists, numofrecs, numofsames):
    global inputs
    artistscores = {}
    for i in range(50):
        artistscores[artists[i]] = (50 - i) * 3
    for i in range(50, 100):
        artistscores[artists[i]] = (100 - i) * 2
    for i in range(100, 150):
        artistscores[artists[i]] = 150 - i
    trackscores = {}
    taglist = list(profile.keys())
    for item in tracks.items():
        trackscores[item[0]] = 1
        for i in range(len(artists)):
            if item[1][0] == artists[i]:
                trackscores[item[0]] = artistscores[artists[i]]
        if tracks[item[0]][1] == taglist[0]:
            trackscores[item[0]] = trackscores[item[0]] * 3
        elif tracks[item[0]][1] == taglist[1]:
            trackscores[item[0]] = trackscores[item[0]] * 2
    sorted_by_score = sorted(trackscores.items(), key=lambda x: x[1], reverse=True)
    i = 0
    while sorted_by_score[i][0] in inputs:
        i = i + 1
    recs = [sorted_by_score[i][0]]
    i = i + 1
    sameartistsongs = 1
    prevartist = sorted_by_score[0][0].split(" - ")[-1]
    while (len(recs) < numofrecs) and (i < len(sorted_by_score)):
        currartist = sorted_by_score[i][0].split(" - ")[-1]
        if currartist != prevartist:
            sameartistsongs = 1
        if (sameartistsongs < numofsames) and (
            (sorted_by_score[i][0] in inputs) == False
        ):
            recs.append(sorted_by_score[i][0])
            i = i + 1
        else:
            i = i + 1
        if currartist == prevartist:
            sameartistsongs = sameartistsongs + 1
        prevartist = currartist
    print(recs)
    return recs


if __name__ == "__main__":
    app.run(debug=True)
