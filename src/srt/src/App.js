import "./App.css";
import * as React from "react";
import "./App.css";
import Rating from "@mui/material/Rating";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Song Recommendation Tool</h1>
      </header>
      <div className="Song Search">
        <p>Song Search</p>
        <input placeholder="Song Name" />
        <input placeholder="Artist" />
        <button>+ Add Song</button>
        <p>Song 1</p>
        <Rating name="simple-controlled" precision={0.5} />
        <button>Remove Song</button>
        <button>Submit</button>
      </div>
    </div>
  );
}

export default App;
