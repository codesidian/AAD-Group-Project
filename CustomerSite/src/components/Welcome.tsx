import * as React from "react";
import TextField from "./TextField";
import { StoresDAO } from "../data/Types";
import * as Config from "../config";

type WelcomeProps = {
    dao: StoresDAO;
    onStart: () => void;
}

type WelcomeState = {
    isBrowserCompatible: boolean;
    errors: Array<string>;
}

export default class Welcome extends React.Component<WelcomeProps, WelcomeState> {
    state = {
        isBrowserCompatible: navigator.mediaDevices !== undefined,
        errors: []
    }

    clickStart = async (e: React.MouseEvent) => {
        e.preventDefault();

        // TODO: version check
        if (await this.props.dao.getVersion() != Config.APP_VERSION) {
            this.setState({errors: ["Application out of date. Please refresh page."]});    
        } else {
            this.props.onStart();
        }
    }

    render() {
        const header = <h1 className="text-center">Welcome to Spicy Stores</h1>;
        const errors = this.state.errors.map(x => <div className="alert alert-danger" role="alert">{x}</div>);

        if (this.state.isBrowserCompatible) {
            return <form>
                {header}
                {errors}
                <input onClick={this.clickStart} className="btn btn-primary" type="submit" value="Start" style={{width: "100%"}} />
            </form>;
        } else {
            return <div>
                {header}
                <p>Your web browser is incompatible with this application.</p>
                <p>TODO: add detail</p>
            </div>;
        }
    }
}
