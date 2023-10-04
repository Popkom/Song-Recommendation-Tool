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
  const [data, setData] = useState("");
  const [messageData, setMessageData] = useState({ message: "" });
  const [isLoading, setIsLoading] = useState(false);
  const addSongComponent = () => {
    sendData();
  };
  const trackChange = (e: ChangeEvent<HTMLInputElement>) => {
    setTrack(e.target.value);
  };
  const artistChange = (e: ChangeEvent<HTMLInputElement>) => {
    setArtist(e.target.value);
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
        <button>Submit</button>
      </div>
    </div>
  );
}

export default App;
