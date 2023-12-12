import requests
import json
from itertools import islice
from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlencode
import time
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)
CORS(app)

API_KEY = "1b5e19b6420f8b125a4f68e3c840eaa3"
useragent = "LIoannou - UofG Song Recommendation Tool"
SpotCID = "074ce5408b5d4e25975ad957adf4b0b9"
SpotSec = "b6fb801c4f7648158208f9c92cf93b5d"
profile = {}
inputs = {}
tagdict = {}
inpartists = []
spoturis = []
errors = []
client_credentials_manager = SpotifyClientCredentials(
    client_id=SpotCID, client_secret=SpotSec
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@app.route("/api/data", methods=["POST"])
def receive_song():
    global inputs
    global profile
    global inpartists
    data = request.json
    if data == "r":
        latest = list(inputs.keys())[-1]
        rating = inputs[latest][3]
        for i in range(3):
            profile[inputs[latest][i]] = profile[inputs[latest][i]] - float(rating)
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
    inputs[respandtrack[1] + " - " + respandtrack[2]] = []
    i = 0
    while i < len(tags) and i < 3:
        inputs[respandtrack[1] + " - " + respandtrack[2]].append(tags[i].split("/")[0])
        i = i + 1
    inputs[respandtrack[1] + " - " + respandtrack[2]].append(songdata[2])
    if respandtrack[2] not in inpartists:
        inpartists.append(respandtrack[2])
    updateprofile(tags, songdata[2])
    return jsonify({"message": respandtrack[1] + " - " + respandtrack[2]})


@app.route("/api/submit-songs", methods=["POST"])
def submit_songs():
    global profile
    global spoturis
    global errors
    data = get_data(profile)
    params = request.json.split("/")
    numofrecs = params[0]
    numfofsames = params[1]
    if len(profile) == 0:
        return jsonify({"message": "Your Taste profile is empty"})
    recs = calcscores(profile, data[0], data[1], int(numofrecs), int(numfofsames))
    spotfunc = get_spot_ids(recs)
    spoturis = spotfunc[0]
    errors = spotfunc[1]
    recsasstring = ", ".join(recs)
    taglist = list(profile.keys())[0:3]
    topthree = " - ".join(taglist)
    reset()
    return jsonify(
        {
            "message": "Recommendations: "
            + recsasstring
            + "\n"
            + "Taste profile: "
            + topthree
        }
    )


@app.route("/api/create-playlist", methods=["POST"])
def create_playlist():
    data = request.json
    authurl = "https://api.spotify.com/v1/me"
    headers = {"Authorization": "Bearer {token}".format(token=data)}
    response = requests.get(authurl, headers=headers)
    actualresp = response.json()
    userid = actualresp["id"]
    createplaylurl = "https://api.spotify.com/v1/users/{user_id}/playlists".format(
        user_id=userid
    )
    body = json.dumps(
        {
            "name": "Song Recommendation Tool",
            "description": "Recommended tracks from the Song Recommendation Tool web app",
            "public": True,
        }
    )
    response = requests.post(url=createplaylurl, data=body, headers=headers)
    playlresp = response.json()
    playlid = playlresp["id"]
    populateplaylurl = (
        "https://api.spotify.com/v1/playlists/{playlist_id}/tracks".format(
            playlist_id=playlid
        )
    )
    body = json.dumps({"uris": spoturis})
    response = requests.post(url=populateplaylurl, data=body, headers=headers)
    errorsmsg = "Spotify errors on the following songs: " + ", ".join(errors)
    print(errorsmsg)
    return jsonify(
        {"message": playlresp["external_urls"]["spotify"], "errors": errorsmsg}
    )


def get_spot_ids(recs):
    authurl = "https://accounts.spotify.com/api/token"
    searchurl = "https://api.spotify.com/v1/search?"
    auth_response = requests.post(
        authurl,
        {
            "grant_type": "client_credentials",
            "client_id": SpotCID,
            "client_secret": SpotSec,
        },
    ).json()
    time.sleep(0.5)
    print(auth_response)
    token = auth_response["access_token"]
    headers = {"Authorization": "Bearer {token}".format(token=token)}
    uris = []
    notfound = []
    for i in range(len(recs)):
        print("case1")
        track = recs[i].split(" - ")[0]
        trackurl = track.replace(" ", "%20")
        artist = recs[i].split(" - ")[1].replace(" ", "%20")
        actualartist = recs[i].split(" - ")[1]
        print(track + " " + actualartist)
        data = urlencode(
            {
                "q": "%20" + "track:" + trackurl + "%20" + "artist:" + artist,
                "type": "track",
                "limit": "50",
            }
        )
        response = requests.get(searchurl + data, headers=headers)
        actualresp = response.json()
        if len(actualresp["tracks"]["items"]) == 0:
            print("no results")
        # print(actualresp["tracks"]["items"][0])
        try:
            j = 0
            match = 0
            while match == 0:
                if (
                    actualresp["tracks"]["items"][j]["name"].casefold()
                    == track.casefold()
                ) and (
                    actualresp["tracks"]["items"][j]["artists"][0]["name"].casefold()
                    == actualartist.casefold()
                ):
                    uris.append(actualresp["tracks"]["items"][j]["uri"])
                    match = 1
                    print("case 1 - match")
                j = j + 1
        except:
            try:
                print("case2 - no search results - search artist")
                data = urlencode(
                    {
                        "q": "%20" + "artist:" + artist,
                        "type": "track",
                        "limit": "100",
                        "offset": "0",
                    }
                )
                response = requests.get(searchurl + data, headers=headers)
                actualresp = response.json()
                match = 0
                for j in range(50):
                    if actualresp["tracks"]["items"][j]["name"] == track:
                        uris.append(actualresp["tracks"]["items"][j]["uri"])
                        print("case2 match")
                        match = 1
                        break
                if match == 0:
                    raise Exception("case2 - no match")
            except:
                try:
                    print("case3 - just track")
                    data = urlencode(
                        {
                            "q": "%20" + "track:" + trackurl,
                            "type": "track",
                            "limit": "50",
                        }
                    )
                    response = requests.get(searchurl + data, headers=headers)
                    actualresp = response.json()
                    # print(actualresp)
                    match = 0
                    for k in range(50):
                        if (
                            (
                                (
                                    actualresp["tracks"]["items"][k]["name"].casefold()
                                    == track.casefold()
                                )
                                and (
                                    actualresp["tracks"]["items"][k]["artists"][0][
                                        "name"
                                    ].casefold()
                                    == actualartist.casefold()
                                )
                            )
                            or (
                                actualresp["tracks"]["items"][k]["name"].casefold()
                                == track.split(" (")[0].casefold()
                            )
                            and (
                                actualresp["tracks"]["items"][k]["artists"][0][
                                    "name"
                                ].casefold()
                                == actualartist.casefold()
                            )
                        ):
                            uris.append(actualresp["tracks"]["items"][k]["uri"])
                            match = 1
                            print("case3 - match")
                            break
                    if match == 0:
                        raise Exception("case3 - no match")
                except:
                    try:
                        print("case4 - lowercase")
                        data = urlencode(
                            {
                                "q": "%20"
                                + "track:"
                                + track.lower().replace(" ", "%20")
                                + "%20"
                                + "artist:"
                                + artist.lower(),
                                "type": "track",
                                "limit": "100",
                            }
                        )
                        print(data)
                        response = requests.get(searchurl + data, headers=headers)
                        actualresp = response.json()
                        match = 0
                        for l in range(50):
                            if (
                                actualresp["tracks"]["items"][l]["name"].casefold()
                                == track.casefold()
                            ) and (
                                actualresp["tracks"]["items"][l]["artists"][0][
                                    "name"
                                ].casefold()
                                == actualartist.casefold()
                            ):
                                uris.append(actualresp["tracks"]["items"][l]["uri"])
                                match = 1
                                print("case4 - match")
                                break
                        if match == 0:
                            raise Exception("case4 - no match")
                    except:
                        try:
                            print("case5 - just artist for top tracks")
                            if actualartist.casefold() == "21 Savage".casefold():
                                artist = "twenty one savage".replace(" ", "%20")
                            data = urlencode(
                                {
                                    "q": "%20" + "artist:" + artist,
                                    "type": "artist",
                                }
                            )
                            response = requests.get(searchurl + data, headers=headers)
                            actualresp = response.json()
                            match = 0
                            for i in range(20):
                                if (
                                    actualresp["artists"]["items"][i]["name"].casefold()
                                    == actualartist.casefold()
                                ):
                                    artistid = actualresp["artists"]["items"][i]["id"]
                                    artisttoptracksurl = "https://api.spotify.com/v1/artists/{id}/top-tracks?market=US".format(
                                        id=artistid
                                    )
                                    response = requests.get(
                                        artisttoptracksurl, headers=headers
                                    )
                                    actualresp = response.json()
                                    for j in range(50):
                                        if (
                                            actualresp["tracks"][j]["name"].casefold()
                                            == track.casefold()
                                        ):
                                            uris.append(actualresp["tracks"][j]["uri"])
                                            match = 1
                                            print("topcase - match")
                                            break
                            if match == 0:
                                raise Exception("no topmatch")
                        except:
                            print("error" + track)
                            notfound.append(track + " - " + actualartist)
        time.sleep(0.5)
    createplaylurl = "https://api.spotify.com/v1/users/popkomm/playlists"
    createplaylbody = json.dumps({"name": "Song Recommendation Tool"})
    response = requests.post(url=createplaylurl, data=createplaylbody, headers=headers)
    return [uris, notfound]


def reset():
    global profile
    global inputs
    global tagdict
    global inpartists
    profile = {}
    inputs = {}
    tagdict = {}
    inpartists = []


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
    for i in range(len(list(profile.keys()))):
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
    for i in range(len(list(profile.keys()))):
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
    i = 0
    while i < len(artists):
        if i < 50:
            artistscores[artists[i]] = (50 - i) * 3
        if i >= 50 and i < 100:
            artistscores[artists[i]] = (100 - i) * 2
        if i >= 100:
            artistscores[artists[i]] = 150 - i
        i = i + 1
    trackscores = {}
    taglist = list(profile.keys())
    for item in tracks.items():
        trackscores[item[0]] = 1
        for i in range(len(artists)):
            if item[1][0] == artists[i]:
                trackscores[item[0]] = artistscores[artists[i]]
        if item[1][0] in inpartists:
            trackscores[item[0]] = trackscores[item[0]] + 150
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
            sameartistsongs = 0
        if (sameartistsongs < numofsames) and (
            (sorted_by_score[i][0] in inputs) == False
        ):
            recs.append(sorted_by_score[i][0])
            sameartistsongs = sameartistsongs + 1
            i = i + 1
        else:
            i = i + 1
        prevartist = currartist
    print(recs)
    return recs


if __name__ == "__main__":
    app.run(debug=True)
