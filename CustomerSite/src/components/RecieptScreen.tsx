import * as React from "react";
import QRScanner from "./QRScanner";
import PressToScan from "./PressToScan";
import { StoresDAO, Sale } from "../data/Types";
import TestDAO from "../data/TestDAO";
import Spinner from "./Spinner";
import ProductTable from "./ProductsTable";

type RecieptScreenProps = {
    sale: Sale;
    onNext: () => void;
}

export default class RecieptScreen extends React.Component<RecieptScreenProps> {
    render() {
        let totalPrice = 0;
        Array.from(this.props.sale.items).forEach(x => totalPrice += x.quantity * x.item.price);

        return <div>
            <h1>Recipet</h1>
            <div>Total price: £{(totalPrice / 100).toFixed(2)}</div>
            <div className="btn-group" role="group" style={{width: "100%"}}>
                <button className="btn btn-primary" onClick={this.props.onNext}>Finish</button>
            </div>
        </div>;
    }
}
