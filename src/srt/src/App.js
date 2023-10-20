import "./App.css";
import * as React from "react";
import "./App.css";
import Rating from "@mui/material/Rating";
import { ChangeEvent, useState, useEffect } from "react";

function App() {
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
  const addSongComponent = () => {
    sendData();
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
    } catch (error) {
      console.error("Error: ", error);
    }
  };
  const sendData = async () => {
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
  useEffect(() => {
    if (messageData.message !== "") {
      setSongComponents((prevComponents) => [
        ...prevComponents,
        [
          <div key={prevComponents.length}>
            <p>{messageData.message}</p>
            <Rating precision={0.5} value={rating} readOnly />
          </div>,
        ],
      ]);
    }
  }, [messageData]);
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
        <button>Remove Song</button>
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
      </div>
    </div>
  );
}

export default App;
