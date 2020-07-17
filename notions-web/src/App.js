import React, { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";
const loadNotions = function (callback) {
  const xhr = new XMLHttpRequest();
  const method = "GET";
  const url = "http://localhost:8000/api/notions/";
  const responseType = "json";
  xhr.responseType = responseType;
  xhr.open(method, url);
  xhr.onload = function () {
    callback(xhr.response, xhr.status);
  };
  xhr.onerror = function (e) {
    console.log(e);
    callback({ message: "The request was an error" }, 400);
  };
  xhr.send();
};
function App() {
  const [notions, setNotions] = useState([]);
  useEffect(() => {
    const myCallback = (response, status) => {
      console.log(response, status);
      if (status === 200) {
        setNotions(response);
      } else {
        console.log("There was an error");
      }
    };
    loadNotions(myCallback);
  }, []);
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>
          {notions.map((notion, index) => {
            return <li>{notion.content}</li>;
          })}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}
export default App;
