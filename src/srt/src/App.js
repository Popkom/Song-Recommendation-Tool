import "./App.css";
import * as React from "react";
import "./App.css";
import Rating from "@mui/material/Rating";
import { ChangeEvent, useState, useEffect } from "react";

function App() {
  const SpotCID = "074ce5408b5d4e25975ad957adf4b0b9";
  const redirect_uri = "http://localhost:3000";
  const auth_endpoint = "https://accounts.spotify.com/authorize";
  const scopes = [
    "user-read-private",
    "user-read-email",
    "playlist-modify-public",
    "playlist-modify-private",
  ];
  const resp_type = "token&show_dialog=true";
  const loginurl = `${auth_endpoint}?client_id=${SpotCID}&redirect_uri=${redirect_uri}&scope=${scopes.join(
    "%20"
  )}&response_type=${resp_type}`;
  const [track, setTrack] = useState("");
  const [artist, setArtist] = useState("");
  const [rating, setRating] = useState(0);
  const [songComponents, setSongComponents] = useState([]);
  const [messageData, setMessageData] = useState({ message: "", empty: "" });
  const [isLoading, setIsLoading] = useState(false);
  const [loadingRecs, setLoadingRecs] = useState(false);
  const [numOfRecs, setNumOfRecs] = useState("");
  const [numOfSames, setNumOfSames] = useState("");
  const [recs, setRecs] = useState({ message: "", taste: "" });
  const [showCreatePlaylist, setShowCreatePlaylist] = useState(false);
  const [loadingPlaylist, setLoadingPlaylist] = useState(false);
  const [playlist, setPlaylist] = useState({ message: "", errors: "" });
  const [createdPlaylist, setCreatedPlaylist] = useState(false);
  const [topTags, setTopTags] = useState({ message: "" });
  const [gotTags, setGotTags] = useState(false);
  const [tagOne, setTagOne] = useState("");
  const [tagTwo, setTagTwo] = useState("");
  const [tagThree, setTagThree] = useState("");
  const [checked, setChecked] = useState(false);
  let loading = false;
  const addSongComponent = () => {
    sendAddData();
  };
  const trackChange = (e: ChangeEvent<HTMLInputElement>) => {
    setTrack(e.target.value);
  };
  const artistChange = (e: ChangeEvent<HTMLInputElement>) => {
    setArtist(e.target.value);
  };
  const numOfRecsChange = (e: ChangeEvent<HTMLInputElement>) => {
    setNumOfRecs(e.target.value);
  };
  const numOfSamesChange = (e: ChangeEvent<HTMLInputElement>) => {
    setNumOfSames(e.target.value);
  };
  const tagOneChange = (e: ChangeEvent<HTMLInputElement>) => {
    setTagOne(e.target.value);
  };
  const tagTwoChange = (e: ChangeEvent<HTMLInputElement>) => {
    setTagTwo(e.target.value);
  };
  const tagThreeChange = (e: ChangeEvent<HTMLInputElement>) => {
    setTagThree(e.target.value);
  };
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setChecked(!checked);
  };
  const submitSongs = async () => {
    try {
      setLoadingRecs(true);
      const response = await fetch("http://localhost:5000/api/submit-songs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(
          numOfRecs +
            "/" +
            numOfSames +
            "/" +
            tagOne +
            "/" +
            tagTwo +
            "/" +
            tagThree +
            "/" +
            checked
        ),
      });

      if (!response.ok) {
        throw new Error("Failed to submit");
      }
      setRecs(await response.json());
      setShowCreatePlaylist(true);
      setLoadingRecs(false);
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  useEffect(() => {
    if (recs.message !== "") {
      window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    }
  }, [recs]);

  const sendAddData = async () => {
    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:5000/api/data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(track + "/" + artist + "/" + rating),
      });
      if (!response.ok) {
        throw new Error("HTTP error! Status: ${response.status}");
      }
      const result = await response.json();
      if (result.message == "404") {
        alert(
          track +
            " - " +
            artist +
            " was not found. Make sure your spellings of song title and artist name are correct."
        );
      } else {
        if (result.message == "dup") {
          alert("Song already added.");
        } else if (result.empty == "yes") {
          alert("No genre tags recorded for this song");
        } else if (result.message == "ratingerror") {
          alert("Invalid rating - Rating must be greater than 0");
        } else {
          setMessageData(result);
        }
      }
    } catch (error) {
      console.error("Error sending data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const sendRemoveData = async () => {
    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:5000/api/data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify("r"),
      });
      if (!response.ok) {
        throw new Error("HTTP error! Status: ${response.status}");
      }
      const result = await response.json();
      if (result.message == "e") {
        alert("No songs to remove");
      }
      setMessageData({ message: "r" });
    } catch (error) {
      console.error("Error sending data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const clearSongs = () => {
    const userConfirmed = window.confirm(
      "Are you sure you want to clear all songs?"
    );
    if (userConfirmed) {
      sendClearData();
    }
  };

  const sendClearData = async () => {
    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:5000/api/data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify("c"),
      });
      if (!response.ok) {
        throw new Error("HTTP error! Status: ${response.status}");
      }
      setMessageData({ message: "c" });
    } catch (error) {
      console.error("Error sending data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const getTokenFromUrl = () => {
    return window.location.hash
      .substring(1)
      .split("&")
      .reduce((initial, item) => {
        let parts = item.split("=");
        initial[parts[0]] = decodeURIComponent(parts[1]);
        return initial;
      }, {});
  };

  useEffect(() => {
    if (
      messageData.message !== "" &&
      messageData.message !== "r" &&
      messageData.message !== "c"
    ) {
      setSongComponents((prevComponents) => [
        ...prevComponents,
        {
          track: messageData.message,
          rating: rating,
        },
      ]);
    } else if (messageData.message == "r") {
      setSongComponents((prevComponents) => {
        if (prevComponents.length > 0) {
          const updatedComponents = [...prevComponents];
          updatedComponents.pop();
          return updatedComponents;
        } else {
          return prevComponents;
        }
      });
    } else if (messageData.message == "c") {
      setSongComponents([]);
    }
  }, [messageData]);

  useEffect(() => {
    const t = getTokenFromUrl().access_token;
    if (
      t &&
      t != "" &&
      t[0] != " " &&
      t != null &&
      !loadingPlaylist &&
      !loading
    ) {
      setLoadingPlaylist(true);
      loading = true;
      const createPlaylist = async () => {
        try {
          console.log("here");
          const response = await fetch(
            "http://localhost:5000/api/create-playlist",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(t),
            }
          );
          if (!response.ok) {
            throw new Error("HTTP error! Status: ${response.status}");
          }
          setPlaylist(await response.json());
        } catch (error) {
          console.error("Error sending data:", error);
        } finally {
          setLoadingPlaylist(false);
          setCreatedPlaylist(true);
          loading = false;
          window.location.hash = "";
        }
      };
      if (!loadingPlaylist) {
        createPlaylist();
      }
    }
  }, []);

  useEffect(() => {
    if (playlist.message !== "") {
      window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    }
  }, [playlist]);

  useEffect(() => {
    const fetchTopTags = async () => {
      try {
        setGotTags(true);
        const response = await fetch(
          "http://localhost:5000/api/fetch-top-tags",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        if (!response.ok) {
          throw new Error("HTTP error! Status: ${response.status}");
        }
        const result = await response.json();
        setTopTags(result);
      } catch (error) {
        console.error("Error fetching top tags: ", error);
      }
    };
    if (gotTags == false) {
      fetchTopTags();
    }
  }, []);

  return (
    <div className="App bg-slate-300 min-h-screen flex flex-col items-center">
      <header className="App-header mt-4">
        <h1 className="text-3xl font-serif">Song Recommendation Tool</h1>
        <h3 className="font-serif">A project by Leonidas Ioannou</h3>
      </header>
      <div className="mx-64 text-center mt-4">
        <p className="text-base font-mono">
          How to use: Enter the title of the song, the name of the artist, and
          your rating of that song in the corresponding input fields, then press
          the Add Song button. Repeat for as many songs as you would like to
          input(the more songs you give, the better recommendations you get!).
          When you’re done entering songs, enter how many recommendations you
          would like, how many recommendations you would like from the same
          artist, if you would like recommendations from artists you input, any
          tags you would like to prioritise, and click Submit!
        </p>
      </div>
      <div className="Song Search items-center mt-4 flex">
        <div className="flex flex-col">
          <p className="mb-1">Song</p>
          <input
            className="mb-4 border rounded"
            value={track}
            onChange={trackChange}
          />
        </div>
        <div className="flex flex-col ml-4">
          <p className="mb-1">Artist</p>
          <input
            className="mb-4 border rounded"
            value={artist}
            onChange={artistChange}
          />
        </div>
        <div className="flex flex-col ml-4 mb-4">
          <p>Rating</p>
          <Rating
            name="controlled"
            precision={0.5}
            value={rating}
            onChange={(event, newRating) => {
              setRating(newRating);
            }}
          />
        </div>
        <div className="flex flex-col ml-4">
          <button
            className="bg-slate-700 text-white px-4 py-2 rounded"
            onClick={addSongComponent}
            disabled={isLoading}
          >
            {isLoading ? "Searching..." : "+Add Song"}
          </button>
        </div>
      </div>
      <div>
        <div className="mx-auto max-w-screen-md mt-4">
          {songComponents.map((component, index) => (
            <div key={index} className="flex items-center mb-4">
              <p className="mr-4">{component.track}</p>
              <Rating precision={0.5} value={component.rating} readOnly />
            </div>
          ))}
        </div>
        <div className="flex justify-center mt-4">
          <button
            className="bg-slate-700 text-white px-4 py-2 rounded"
            onClick={sendRemoveData}
            disabled={isLoading}
          >
            {isLoading ? "Removing..." : "Remove Song"}
          </button>
          <button
            className="bg-slate-700 text-white px-4 py-2 rounded ml-4"
            onClick={clearSongs}
            disabled={isLoading}
          >
            {isLoading ? "Clearing..." : "Clear Songs"}
          </button>
        </div>
        <div className="flex items-center justify-center mt-6 mr-96">
          <p className="mr-4">Enter number of recommendations to get:</p>
          <input
            className="border rounded"
            value={numOfRecs}
            onChange={numOfRecsChange}
          />
        </div>
        <div className="flex items-center justify-center mt-4 mr-14">
          <p className="mr-4">
            How many recommendations from the same artist should be
            allowed?(Recommended: 2)
          </p>
          <input
            className="border rounded"
            value={numOfSames}
            onChange={numOfSamesChange}
          />
        </div>
        <div className="flex items-center justify-center mt-4 mr-14">
          <p className="mr-4">
            Allow recommendations from artists you have input?
          </p>
          <input
            type="checkbox"
            value={checked}
            onChange={handleChange}
            className="rounded-md w-6 h-6"
          ></input>
        </div>
        <div className="mx-64 text-center mt-4">
          <p className="text-base font-mono">Popular tags: {topTags.message}</p>
        </div>
        <div className="flex flex-col items-center mt-4">
          <p className="mb-1">
            (Optional) Enter three or less genre tags you would like to
            prioritise:
          </p>
          <div className="flex mt-2">
            <input
              className="border rounded"
              placeholder="Tag 1"
              value={tagOne}
              onChange={tagOneChange}
            ></input>
            <input
              className="ml-4 border rounded"
              placeholder="Tag 2"
              value={tagTwo}
              onChange={tagTwoChange}
            ></input>
            <input
              className="ml-4 border rounded"
              placeholder="Tag 3"
              value={tagThree}
              onChange={tagThreeChange}
            ></input>
          </div>
        </div>
        <div className="flex justify-center mt-8">
          <button
            className="bg-slate-700 text-white px-4 py-2 rounded w-36"
            onClick={submitSongs}
            disabled={loadingRecs}
          >
            {loadingRecs ? "Submitting..." : "Submit"}
          </button>
        </div>
        <div className="mx-64 text-center mt-4">
          <p className="text-base font-mono">{recs.message}</p>
          <p className="text-base font-mono mt-2">{recs.taste}</p>
        </div>
        <div className="flex justify-center mt-4 mb-8">
          {showCreatePlaylist && (
            <button className="bg-slate-700 text-white px-4 py-2 rounded">
              <a href={loginurl} target="_blank">
                {loadingPlaylist
                  ? "Creating a Spotify Playlist.. Please Wait"
                  : "Create a Spotify Playlist"}
              </a>
            </button>
          )}
        </div>
        <div className="flex flex-col items-center mt-4 mb-8">
          {createdPlaylist && (
            <button className="bg-slate-700 text-white px-4 py-2 rounded">
              <a href={playlist.message} target="_blank">
                {createdPlaylist ? "Link to Playlist" : ""}
              </a>
            </button>
          )}
          <p className="text-base font-mono mt-2">
            {createdPlaylist ? playlist.errors : ""}
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
