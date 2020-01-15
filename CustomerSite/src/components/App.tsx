import * as React from "react";
import Welcome from "./Welcome";
import ScanningScreen from "./ScanningScreen";

type AppProps = {

}

enum Stage {
    Start,
    Scanning,
    Overview,
    Purchasing,
    Recipt
}

type AppState = {
    stage: Stage;
    accountNumber: string;
}

export default class App extends React.Component<AppProps, AppState> {
    state = {
        stage: Stage.Start,
        accountNumber: ''
    }

    changeStage = (newStage: Stage) => {
        console.log("Stage change to " + Stage[newStage]);
        this.setState({
            stage: newStage
        });
    }

    handleAccountNumberChange = (accountNumber: string) => {
        this.setState({
            accountNumber: accountNumber
        });
    }

    render() {
        switch (this.state.stage) {
            case Stage.Start:
                const accountNumber = this.state.accountNumber;
                return <Welcome
                    accountNumber={accountNumber}
                    onAccountNumberChange={this.handleAccountNumberChange}
                    onStart={() => this.changeStage(Stage.Scanning)}
                />;
            case Stage.Scanning:
                return <ScanningScreen />;
            default:
                return <div>
                    <div>Roses are red</div>
                    <div>Violets are blue</div>
                    <div>This app has crashed</div>
                    <div>Please refresh page</div>
                </div>;
        }
    }
}
