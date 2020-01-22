import * as React from "react";
import * as ReactDOM from "react-dom";

import App from "./components/App";
import TestDAO from "./data/TestDAO";

(function () {
    let app = document.getElementById("app");
    ReactDOM.render(<App dao={new TestDAO()} />, app);
})();
