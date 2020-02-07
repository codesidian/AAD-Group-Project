import * as React from "react";
import Cart from "../data/Cart";
import { SaleItem } from "../data/Types";
import SpinNumber from "./SpinNumber";

type ProductRowProps = {
    item: SaleItem;
    edit?: (code: string, quantity: number) => void;
};

export default class ProductRow extends React.Component<ProductRowProps> {
    onQuantityBlur = (e: React.FocusEvent<HTMLInputElement>) => {
        const edit = this.props.edit;
        if (edit !== undefined) {
            edit(this.props.item.item.code, e.target.valueAsNumber)
        }
    }

    onQuantityChange = (value: number) => {
        const edit = this.props.edit;
        if (edit !== undefined) {
            edit(this.props.item.item.code, value)
        }
    }

    render() {
        const item = this.props.item;
        const quantity : JSX.Element = (() => {
            if (this.props.edit !== undefined) {
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
