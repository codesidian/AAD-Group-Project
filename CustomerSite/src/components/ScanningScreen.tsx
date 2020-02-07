import * as React from "react";
import QRScanner from "./QRScanner";
import PressToScan from "./PressToScan";
import { StoresDAO } from "../data/Types";
import TestDAO from "../data/TestDAO";
import Spinner from "./Spinner";
import Cart from "../data/Cart";
import ProductTable from "./ProductsTable";

type ScanningScreenProps = {
    dao: StoresDAO;
    cart: Cart;
    onNext: () => void;
}

enum State {
    Waiting,
    Scanning,
    Loading,
}

type ScanningScreenState = {
    state: State;
    cancelTimeout?: ReturnType<typeof setTimeout>;
}

export default class ScanningScreen extends React.Component<ScanningScreenProps, ScanningScreenState> {
    state: ScanningScreenState = {
        state: State.Waiting
    }

    showScanner = () => {
        const timeout = setTimeout(this.cancelScanner, 30000);
        this.setState({state: State.Scanning, cancelTimeout: timeout});
    }

    cancelScanner = () => {
        this.setState({state: State.Waiting, cancelTimeout: undefined});
    }

    codeScanned = async (code: string) => {
        console.log("Scanned", code);
        if (this.state.cancelTimeout !== undefined) {
            clearTimeout(this.state.cancelTimeout);
        }
        this.setState({state: State.Loading, cancelTimeout: undefined});

        try {
            let item = await this.props.dao.getItem(code);
            this.props.cart.addItem(item);
        } catch (error) {
            alert(error);
        }

        this.setState({state: State.Waiting});
    }

    render() {
        const currentScreen = (() => {
            switch (this.state.state) {
                case State.Waiting:
                    return <PressToScan pressed={this.showScanner} />
                case State.Scanning:
                    return <QRScanner qrScanned={this.codeScanned} />
                case State.Loading:
                    return <Spinner />
                default:
                    return <div>Invalid state</div>
            }
        })();
        return <div>
            {currentScreen}
            <ProductTable items={this.props.cart.getItems()} edit={this.props.cart.setItemQuantity} />
            <button className="btn btn-primary" onClick={this.props.onNext} style={{width: "100%"}}>Next</button>
        </div>;
    }
}
