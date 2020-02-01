import * as React from "react";
import Welcome from "./Welcome";
import ScanningScreen from "./ScanningScreen";
import { StoresDAO } from "../data/Types";

type AppProps = {
    dao: StoresDAO;
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
}

export default class App extends React.Component<AppProps, AppState> {
    state = {
        stage: Stage.Start,
    }

    changeStage = (newStage: Stage) => {
        console.log("Stage change to " + Stage[newStage]);
        this.setState({
            stage: newStage
        });
    }

    render() {
        const dao = this.props.dao;
        switch (this.state.stage) {
            case Stage.Start:
                return <Welcome
                    dao={dao}
                    onStart={() => this.changeStage(Stage.Scanning)}
                />;
            case Stage.Scanning:
                return <ScanningScreen
                    dao={dao}
                />;
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
