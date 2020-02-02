import * as React from "react";
import Cart from "../data/Cart";
import { SaleItem } from "../data/Types";
import ProductRow from "./ProductRow";

type ProductTableProps = {
    cart: Cart;
    editable: boolean;
};

export default class ProductTable extends React.Component<ProductTableProps> {
    render() {
        const rows = Array.from(this.props.cart.getItems()).map(
            x => <ProductRow key={x.item.code} cart={this.props.cart} editable={this.props.editable} item={x} />
        )
        return <table className="table">
            <thead>
                <tr><th>Name</th><th>Quantity</th><th>Price</th></tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    }
}
