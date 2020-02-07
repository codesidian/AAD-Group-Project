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
        let totalPrice = 0;
        Array.from(this.props.cart.getItems()).forEach(x => totalPrice += x.quantity * x.item.price);

        return <div>
            <h1>Overview</h1>
            <ProductTable items={this.props.cart.getItems()} />
            <div>Total price: £{(totalPrice / 100).toFixed(2)}</div>
            <div className="btn-group" role="group" style={{width: "100%"}}>
                <button className="btn btn-secondary" onClick={this.props.onBack}>Back</button>
                <button className="btn btn-primary" onClick={this.props.onNext}>Checkout</button>
            </div>
        </div>;
    }
}
