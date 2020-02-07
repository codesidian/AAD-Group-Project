import * as React from "react";
import { StoresDAO, Sale } from "../data/Types";
import Spinner from "./Spinner";
import Cart from "../data/Cart";

type PurchasingScreenProps = {
    dao: StoresDAO;
    cart: Cart;
    onNext: (sale: Sale) => void;
    onBack: () => void;
}

export default class PurchasingScreen extends React.Component<PurchasingScreenProps> {
    doPurchase = async () => {
        try {
            let sale = await this.props.dao.checkout(this.props.cart.getItems());
            this.props.cart.clear();
            this.props.onNext(sale);
        } catch (error) {
            console.error(error);
            alert("An error has occured while trying to process your transaction. Please try again later.");
            this.props.onBack();
        }
    };

    render() {
        return <div>
            <h1>Purchasing</h1>
            <Spinner/>
            <p className="text-center">This may take a moment</p>
        </div>;
    }

    componentDidMount() {
        setTimeout(this.doPurchase, 0);
    }
}
