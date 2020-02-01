import * as React from "react";

export default class Spinner extends React.Component {
    render() {
        return  <div className="text-center">
                    <div className="spinner-border" style={{width: "5em", height: "5em"}} role="status">
                        <span className="sr-only">Loading...</span>
                    </div>
                </div>
    }
}
