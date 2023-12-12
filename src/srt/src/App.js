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
  const [messageData, setMessageData] = useState({ message: "" });
  const [isLoading, setIsLoading] = useState(false);
  const [loadingRecs, setLoadingRecs] = useState(false);
  const [numOfRecs, setNumOfRecs] = useState("");
  const [numOfSames, setNumOfSames] = useState("");
  const [recs, setRecs] = useState({ message: "" });
  const [showCreatePlaylist, setShowCreatePlaylist] = useState(false);
  const [loadingPlaylist, setLoadingPlaylist] = useState(false);
  const [playlist, setPlaylist] = useState({ message: "", errors: "" });
  const [createdPlaylist, setCreatedPlaylist] = useState(false);
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
  const submitSongs = async () => {
    try {
      setLoadingRecs(true);
      const response = await fetch("http://localhost:5000/api/submit-songs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(numOfRecs + "/" + numOfSames),
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
      setMessageData(result);
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
        [
          <div key={prevComponents.length}>
            <p>{messageData.message}</p>
            <Rating precision={0.5} value={rating} readOnly />
          </div>,
        ],
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
  return (
    <div className="App">
      <header className="App-header">
        <h1>Song Recommendation Tool</h1>
      </header>
      <div className="Song Search">
        <p>Song Search</p>
        <input placeholder="Song Name" value={track} onChange={trackChange} />
        <input placeholder="Artist" value={artist} onChange={artistChange} />
        <Rating
          name="controlled"
          precision={0.5}
          value={rating}
          onChange={(event, newRating) => {
            setRating(newRating);
          }}
        />
        <button onClick={addSongComponent} disabled={isLoading}>
          {isLoading ? "Searching..." : "+Add Song"}
        </button>
        <div>
          {songComponents.map((component, index) => (
            <div key={index}>{component}</div>
          ))}
        </div>
        <button onClick={sendRemoveData} disabled={isLoading}>
          {isLoading ? "Removing..." : "Remove Song"}
        </button>
        <button onClick={clearSongs} disabled={isLoading}>
          {isLoading ? "Clearing..." : "Clear Songs"}
        </button>
        <p>Enter number of recommendations to get:</p>
        <input
          placeholder="Number of recommendations"
          value={numOfRecs}
          onChange={numOfRecsChange}
        />
        <p>
          How many recommendations from the same artist should be
          allowed?(Recommended: 2)
        </p>
        <input
          placeholder="Same artist recs"
          value={numOfSames}
          onChange={numOfSamesChange}
        />
        <button onClick={submitSongs} disabled={loadingRecs}>
          {loadingRecs ? "Submitting..." : "Submit"}
        </button>
        {recs.message}
        {showCreatePlaylist && (
          <button>
            <a href={loginurl} target="_blank">
              {loadingPlaylist
                ? "Creating a Spotify Playlist.. Please Wait"
                : "Create a Spotify Playlist"}
            </a>
          </button>
        )}
        <a href={playlist.message} target="_blank">
          {createdPlaylist ? "Link to Playlist" : ""}
        </a>
        <p>{createdPlaylist ? playlist.errors : ""}</p>
      </div>
    </div>
  );
}

export default App;
