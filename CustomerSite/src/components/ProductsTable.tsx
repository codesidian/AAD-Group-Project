import * as React from "react";
import Cart from "../data/Cart";
import { SaleItem } from "../data/Types";
import ProductRow from "./ProductRow";

type ProductTableProps = {
    items: ArrayLike<SaleItem>;
    edit?: (code: string, quantity: number) => void;
};

export default class ProductTable extends React.Component<ProductTableProps> {
    render() {
        const rows = Array.from(this.props.items).map(
            x => <ProductRow key={x.item.code} edit={this.props.edit} item={x} />
        );
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
