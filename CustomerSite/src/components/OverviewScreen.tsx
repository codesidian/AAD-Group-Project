import * as React from "react";
import QRScanner from "./QRScanner";
import PressToScan from "./PressToScan";
import { StoresDAO } from "../data/Types";
import TestDAO from "../data/TestDAO";
import Spinner from "./Spinner";
import Cart from "../data/Cart";
import ProductTable from "./ProductsTable";

type OverviewScreenProps = {
    dao: StoresDAO;
    cart: Cart;
    onNext: () => void;
    onBack: () => void;
}

export default class OverviewScreen extends React.Component<OverviewScreenProps> {
    render() {
        return <div>
            <h1>Overview</h1>
            <ProductTable cart={this.props.cart} editable={false} />
            <div className="btn-group" role="group" style={{width: "100%"}}>
                <button className="btn btn-secondary" onClick={this.props.onBack}>Back</button>
                <button className="btn btn-primary" onClick={this.props.onNext}>Next</button>
            </div>
        </div>;
    }
}
