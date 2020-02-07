import * as React from "react";
import * as ReactDOM from "react-dom";

import App from "./components/App";
import RemoteDAO from "./data/RemoteDAO";

(function () {
    let app = document.getElementById("app");
    ReactDOM.render(<App dao={new RemoteDAO()} />, app);
})();
