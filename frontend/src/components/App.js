import React, { Component } from "react";
import { render } from "react-dom";

export default class App extends Component {
  // eslint-disable-next-line no-useless-constructor
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div>
        <h1>yo</h1>
      </div>
    );
  }
}
const appDiv = document.getElementById("app");

render(<App></App>, appDiv);
