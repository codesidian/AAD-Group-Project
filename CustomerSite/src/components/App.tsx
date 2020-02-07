import * as React from "react";
import Welcome from "./Welcome";
import ScanningScreen from "./ScanningScreen";
import { StoresDAO, Sale } from "../data/Types";
import ObservableCart from "../data/ObservableCart";
import MemoryCart from "../data/MemoryCart";
import OverviewScreen from "./OverviewScreen";
import PurchasingScreen from "./PurchasingScreen";
import RecieptScreen from "./RecieptScreen";

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
    cart: ObservableCart;
    sale?: Sale;
}

export default class App extends React.Component<AppProps, AppState> {
    state: AppState = {
        stage: Stage.Start,
        cart: new ObservableCart(new MemoryCart()),
    }

    changeStage = (newStage: Stage) => {
        console.log("Stage change to " + Stage[newStage]);
        this.setState({
            stage: newStage
        });
    }

    cartUpdated = (cart: ObservableCart) => {
        this.setState({ cart: cart });
    }

    render() {
        const dao = this.props.dao;
        const cart = this.state.cart;
        switch (this.state.stage) {
            case Stage.Start:
                return <Welcome
                    dao={dao}
                    onStart={() => this.changeStage(Stage.Scanning)}
                />;
            case Stage.Scanning:
                return <ScanningScreen
                    dao={dao}
                    cart={cart}
                    onNext={() => this.changeStage(Stage.Overview)}
                />;
            case Stage.Overview:
                return <OverviewScreen
                    dao={dao}
                    cart={cart}
                    onNext={() => this.changeStage(Stage.Purchasing)}
                    onBack={() => this.changeStage(Stage.Scanning)}
                />;
            case Stage.Purchasing:
                return <PurchasingScreen
                    dao={dao}
                    cart={cart}
                    onNext={(sale) => { this.setState({sale: sale}); this.changeStage(Stage.Recipt); }}
                    onBack={() => this.changeStage(Stage.Overview)}
                />;
            case Stage.Recipt:
                return <RecieptScreen
                    sale={this.state.sale as Sale}
                    onNext={() => this.changeStage(Stage.Start)}
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

    componentDidMount() {
        this.state.cart.addObserver(this.cartUpdated);
    }
}
