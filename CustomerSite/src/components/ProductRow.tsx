import * as React from "react";
import Cart from "../data/Cart";
import { SaleItem } from "../data/Types";
import SpinNumber from "./SpinNumber";

type ProductRowProps = {
    cart: Cart;
    editable: boolean;
    item: SaleItem;
};

export default class ProductRow extends React.Component<ProductRowProps> {
    onQuantityBlur = (e: React.FocusEvent<HTMLInputElement>) => {
        this.props.cart.setItemQuantity(this.props.item.item.code, e.target.valueAsNumber);
    }

    onQuantityChange = (value: number) => {
        this.props.cart.setItemQuantity(this.props.item.item.code, value);
    }

    render() {
        const item = this.props.item;
        const quantity : JSX.Element = (() => {
            console.log(this.props.editable);
            if (this.props.editable) {
                return <td><SpinNumber value={item.quantity} onValueChange={this.onQuantityChange}/></td>;
            } else {
                return <td>{item.quantity}</td>;
            }
        })();
        return <tr>
            <td>{item.item.name}</td>
            {quantity}
            <td>£{(item.quantity * item.item.price / 100).toFixed(2)}</td>
        </tr>
    }
}
