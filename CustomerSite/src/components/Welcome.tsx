import * as React from "react";
import TextField from "./TextField";

type WelcomeProps = {
    onStart: () => void;
    accountNumber: string;
    onAccountNumberChange: (accountNumber: string) => void;
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

    clickStart = (e: React.MouseEvent) => {
        e.preventDefault();

        // TODO: version check
        if (false) {
            this.setState({errors: ["Application out of date. Please refresh page."]});    
        } else {
            this.props.onStart();
        }
    }

    render() {
        const accountNumber = this.props.accountNumber;
        const onAccountNumberChange = this.props.onAccountNumberChange;

        const header = <h1 className="text-center">Welcome to Spicy Stores</h1>;
        const errors = this.state.errors.map(x => <div className="alert alert-danger" role="alert">{x}</div>);
        console.log(errors);

        if (this.state.isBrowserCompatible) {
            return <form>
                {header}
                {errors}
                <TextField label="Account number" text={accountNumber} onTextChange={onAccountNumberChange} />
                <input onClick={this.clickStart} className="btn btn-primary" type="submit" value="Start" />
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
