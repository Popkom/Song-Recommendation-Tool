import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlencode
import time
import random

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
similars = {}


# Function to receive either added song, remove latest song, or clear songs
@app.route("/api/data", methods=["POST"])
def receive_song():
    global inputs
    global profile
    global inpartists
    data = request.json
    # remove song button
    if data == "r":
        try:
            latest = list(inputs.keys())[-1]
            rating = inputs[latest][3]
            for i in range(3):
                profile[inputs[latest][i]] = profile[inputs[latest][i]] - float(rating)
            inputs.pop(latest)
            sortedprof = sorted(profile.items(), key=lambda x: x[1], reverse=True)
            profile = dict(sortedprof)
            return jsonify({"message": "Success"})
        except:
            return jsonify({"message": "e"})
    # clear songs button
    if data == "c":
        reset()
        return jsonify({"message": "Success"})
    # add song button
    songdata = data.split("/")
    print(songdata[2])
    if (songdata[2] == "null") or (songdata[2] == "0"):
        return jsonify({"message": "ratingerror"})
    respandtrack = lastfm_get({"track": songdata[0], "artist": songdata[1]})
    if respandtrack == "Song not found":
        return jsonify({"message": "404"})
    if (respandtrack[1] + " - " + respandtrack[2]) in inputs:
        return jsonify({"message": "dup"})
    tags = gettags(respandtrack[0])
    inputs[respandtrack[1] + " - " + respandtrack[2]] = []
    lastfm_similar({"track": respandtrack[1], "artist": respandtrack[2]})
    i = 0
    while i < len(tags) and i < 3:
        inputs[respandtrack[1] + " - " + respandtrack[2]].append(tags[i].split("/")[0])
        i = i + 1
    inputs[respandtrack[1] + " - " + respandtrack[2]].append(songdata[2])
    if respandtrack[2] not in inpartists:
        inpartists.append(respandtrack[2])
    updateprofile(tags, songdata[2])
    if len(tags) != 0:
        return jsonify({"message": respandtrack[1] + " - " + respandtrack[2]})
    else:
        return jsonify(
            {"message": respandtrack[1] + " - " + respandtrack[2], "empty": "yes"}
        )


# Function to handle submit button press
@app.route("/api/submit-songs", methods=["POST"])
def submit_songs():
    global profile
    global spoturis
    global errors
    # get other parameters
    params = request.json.split("/")
    numofrecs = params[0]
    numofsames = params[1]
    priotags = [params[2], params[3], params[4]]
    allowrecsfrominp = params[5]
    # boost score of user-prioritised tags
    for i in range(3):
        for j in range(len(profile.keys())):
            if priotags[i].casefold() == list(profile.keys())[j].casefold():
                profile[list(profile.keys())[j]] = (
                    profile[list(profile.keys())[j]] + 150
                )
    sortedprof = sorted(profile.items(), key=lambda x: x[1], reverse=True)
    profile = dict(sortedprof)
    data = get_data(profile)
    if len(profile) == 0:
        return jsonify({"message": "Your Taste profile is empty"})
    try:
        numofrecsint = int(numofrecs)
        if numofrecsint <= 0:
            return jsonify({"message": "Invalid number of recommendations"})
    except:
        return jsonify({"message": "Invalid number of recommendations"})
    try:
        numofsamesint = int(numofsames)
        if numofsamesint <= 0:
            return jsonify(
                {
                    "message": "Invalid number of recommendations from the same artist to be allowed"
                }
            )
    except:
        return jsonify(
            {
                "message": "Invalid number of recommendations from the same artist to be allowed"
            }
        )
    # get recommendations
    recs = calcscores(
        profile,
        data[0],
        data[1],
        int(numofrecs),
        int(numofsames),
        allowrecsfrominp,
    )
    # get spotify track ids and any errors
    spotfunc = get_spot_ids(recs)
    spoturis = spotfunc[0]
    errors = spotfunc[1]
    # organise recommendations to send back
    recsasstring = ", ".join(recs)
    taglist = list(profile.keys())[0:3]
    topthree = " - ".join(taglist)
    reset()
    return jsonify(
        {
            "message": "Recommendations: " + recsasstring,
            "taste": "Taste profile: " + topthree,
        }
    )


# function to handle create playlist button press
@app.route("/api/create-playlist", methods=["POST"])
def create_playlist():
    # Get user authorisation
    data = request.json
    authurl = "https://api.spotify.com/v1/me"
    headers = {"Authorization": "Bearer {token}".format(token=data)}
    response = requests.get(authurl, headers=headers)
    actualresp = response.json()
    # Create the playlist
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
    # Populate playlist with tracks
    populateplaylurl = (
        "https://api.spotify.com/v1/playlists/{playlist_id}/tracks".format(
            playlist_id=playlid
        )
    )
    body = json.dumps({"uris": spoturis})
    response = requests.post(url=populateplaylurl, data=body, headers=headers)
    errorsmsg = "Spotify errors on the following songs: " + ", ".join(errors)
    print(errorsmsg)
    # Return link to playlist, any errors
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
    # uris is a list for the spotify track ids
    uris = []
    # notfound is for the spotify error tracks
    notfound = []
    for i in range(len(recs)):
        # First spotify search case - track + artist
        track = recs[i].split(" - ")[0]
        trackurl = track.replace(" ", "%20")
        artisturl = recs[i].split(" - ")[1].replace(" ", "%20")
        artist = recs[i].split(" - ")[1]
        print(track + " " + artist)
        print("case1")
        data = urlencode(
            {
                "q": "%20" + "track:" + trackurl + "%20" + "artist:" + artisturl,
                "type": "track",
                "limit": "50",
            }
        )
        response = requests.get(searchurl + data, headers=headers)
        actualresp = response.json()
        if len(actualresp["tracks"]["items"]) == 0:
            print("no results")
        try:
            j = 0
            match = 0
            while match == 0:
                if (
                    actualresp["tracks"]["items"][j]["name"].casefold()
                    == track.casefold()
                ) and (
                    actualresp["tracks"]["items"][j]["artists"][0]["name"].casefold()
                    == artist.casefold()
                ):
                    uris.append(actualresp["tracks"]["items"][j]["uri"])
                    match = 1
                    print("case 1 - match")
                j = j + 1
        except:
            try:
                # Second case - just artist
                print("case2 - no search results - search artist")
                data = urlencode(
                    {
                        "q": "%20" + "artist:" + artisturl,
                        "type": "track",
                        "limit": "100",
                        "offset": "0",
                    }
                )
                response = requests.get(searchurl + data, headers=headers)
                actualresp = response.json()
                match = 0
                for j in range(50):
                    if (
                        actualresp["tracks"]["items"][j]["name"].casefold()
                        == track.casefold()
                    ):
                        uris.append(actualresp["tracks"]["items"][j]["uri"])
                        print("case2 match")
                        match = 1
                        break
                if match == 0:
                    raise Exception("case2 - no match")
            except:
                try:
                    # Third case - just track name
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
                                    == artist.casefold()
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
                                == artist.casefold()
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
                        # Fourth case - force lowercase search
                        print("case4 - lowercase")
                        data = urlencode(
                            {
                                "q": "%20"
                                + "track:"
                                + track.lower().replace(" ", "%20")
                                + "%20"
                                + "artist:"
                                + artist.lower().replace(" ", "%20"),
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
                                == artist.casefold()
                            ):
                                uris.append(actualresp["tracks"]["items"][l]["uri"])
                                match = 1
                                print("case4 - match")
                                break
                        if match == 0:
                            raise Exception("case4 - no match")
                    except:
                        try:
                            # Fifth case - use top tracks method after getting artist id
                            print("case5 - just artist for top tracks")
                            data = urlencode(
                                {
                                    "q": "%20" + "artist:" + artisturl,
                                    "type": "artist",
                                }
                            )
                            response = requests.get(searchurl + data, headers=headers)
                            actualresp = response.json()
                            match = 0
                            for i in range(20):
                                if (
                                    actualresp["artists"]["items"][i]["name"].casefold()
                                    == artist.casefold()
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
                            # No workaround worked
                            print("error " + track)
                            notfound.append(track + " - " + artist)
        time.sleep(0.5)
    return [uris, notfound]


# Function to reset app
def reset():
    global profile
    global inputs
    global tagdict
    global inpartists
    global similars
    profile = {}
    inputs = {}
    tagdict = {}
    inpartists = []
    similars = {}


# Get proper track information and tags of track from last.fm API
def lastfm_get(payload):
    url = "https://ws.audioscrobbler.com/2.0"

    payload["api_key"] = API_KEY
    payload["format"] = "json"
    payload["method"] = "track.search"
    payload["autocorrect"] = "1"
    response = requests.get(url, params=payload)
    jsonresp = response.json()
    try:
        payload["track"] = jsonresp["results"]["trackmatches"]["track"][0]["name"]
        payload["artist"] = jsonresp["results"]["trackmatches"]["track"][0]["artist"]
        payload["method"] = "track.gettoptags"
        response = requests.get(url, params=payload)
        return [response, payload["track"], payload["artist"]]
    except:
        return "Song not found"


def lastfm_similar(payload):
    global similars
    url = "https://ws.audioscrobbler.com/2.0"
    payload["api_key"] = API_KEY
    payload["method"] = "track.getsimilar"
    payload["format"] = "json"
    payload["limit"] = 5
    response = requests.get(url, params=payload)
    jsonresp = response.json()
    if len(jsonresp["similartracks"]["track"]) > 0:
        for i in range(len(jsonresp["similartracks"]["track"])):
            track = (
                jsonresp["similartracks"]["track"][i]["name"]
                + " - "
                + jsonresp["similartracks"]["track"][i]["artist"]["name"]
            )
            if track in similars:
                similars[track] += 1
            else:
                similars[track] = 1


# Get most popular last.fm tags
@app.route("/api/fetch-top-tags", methods=["POST"])
def fetch_top_lastfm_tags():
    url = "https://ws.audioscrobbler.com/2.0"
    payload = {}
    payload["api_key"] = API_KEY
    payload["format"] = "json"
    payload["method"] = "tag.getTopTags"
    response = requests.get(url, params=payload)
    jsonresp = response.json()
    tags = []
    for i in range(20):
        tags.append(jsonresp["toptags"]["tag"][i]["name"])
    tagstring = ", ".join(tags)
    return jsonify({"message": tagstring})


# Get the top three tags of a track, excluding any that are not actual genre tags
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
                tags.append(currenttag + "/" + (str(tagslist[i]["count"])))
    return tags


# Update profile with current tag scores
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


# Get the top tracks for each tag in the user's profile
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


# Calculate the score for each track, create list of recommendations with highest scoring tracks
def calcscores(profile, tracks, artists, numofrecs, numofsames, allowinps):
    global inputs
    artistscores = {}
    recartists = {}
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
        if item[0] in similars:
            trackscores[item[0]] = trackscores[item[0]] + 100 * similars[item[0]]
    sorted_by_score = sorted(trackscores.items(), key=lambda x: x[1], reverse=True)
    i = 0
    while (sorted_by_score[i][0] in inputs) or (
        (sorted_by_score[i][0].split(" - ")[-1] in inpartists)
        and (allowinps == "false")
    ):
        i = i + 1
    recs = [sorted_by_score[i][0]]
    recartists[sorted_by_score[i][0].split(" - ")[-1]] = 1
    i = i + 1
    while (len(recs) < numofrecs) and (i < len(sorted_by_score)):
        currartist = sorted_by_score[i][0].split(" - ")[-1]
        if not currartist in recartists:
            recartists[sorted_by_score[i][0].split(" - ")[-1]] = 0
        if (recartists[sorted_by_score[i][0].split(" - ")[-1]] < numofsames) and (
            (sorted_by_score[i][0] in inputs) == False
        ):
            if (currartist in inpartists) and (allowinps == "false"):
                i = i + 1
            else:
                recs.append(sorted_by_score[i][0])
                recartists[sorted_by_score[i][0].split(" - ")[-1]] = (
                    recartists[sorted_by_score[i][0].split(" - ")[-1]] + 1
                )
                i = i + 1
        else:
            i = i + 1
    print(recs)
    return recs


if __name__ == "__main__":
    app.run(debug=True)
