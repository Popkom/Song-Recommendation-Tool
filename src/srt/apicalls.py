import requests
import json
from itertools import islice
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

API_KEY = "1b5e19b6420f8b125a4f68e3c840eaa3"
useragent = "LIoannou - UofG Song Recommendation Tool"
profile = {}


@app.route("/api/data", methods=["POST"])
def receive_song():
    data = request.json
    songdata = data.split("/")
    respandtrack = lastfm_get({"track": songdata[0], "artist": songdata[1]})
    updateprofile(gettags(respandtrack[0]), songdata[2])
    return jsonify({"message": respandtrack[1] + " - " + respandtrack[2]})


def lastfm_get(payload):
    # headers = {"user-agent": useragent}
    url = "https://ws.audioscrobbler.com/2.0"

    payload["api_key"] = API_KEY
    payload["format"] = "json"
    payload["method"] = "track.search"
    payload["autocorrect"] = "1"
    response = requests.get(url, params=payload)
    jsonresp = response.json()
    # print(jsonresp["results"]["trackmatches"])
    payload["track"] = jsonresp["results"]["trackmatches"]["track"][0]["name"]
    payload["artist"] = jsonresp["results"]["trackmatches"]["track"][0]["artist"]
    payload["method"] = "track.gettoptags"
    response = requests.get(url, params=payload)
    return [response, payload["track"], payload["artist"]]


def gettags(resp):
    actual = resp.json()
    tagslist = actual["toptags"]["tag"]
    tags = []
    i = 0
    if len(tagslist) >= 3:
        while (len(tags) < 3) and (i < len(tagslist)):
            currenttag = tagslist[i]["name"]
            if (currenttag[0] != "-") and (currenttag != "MySpotigramBot"):
                tags.append(currenttag)
            i = i + 1
    else:
        for j in range(len(tagslist)):
            currenttag = tagslist[i]["name"]
            if (currenttag[0] != "-") and (currenttag != "MySpotigramBot"):
                tags.append(currenttag)
    return tags


def updateprofile(tags, rating):
    global profile
    for i in range(len(tags)):
        if tags[i] in profile:
            profile[tags[i]] = profile[tags[i]] + float(rating)
        else:
            profile[tags[i]] = float(rating)
    sortedprof = sorted(profile.items(), key=lambda x: x[1], reverse=True)
    profile = dict(sortedprof)
    print(profile)


if __name__ == "__main__":
    app.run(debug=True)
