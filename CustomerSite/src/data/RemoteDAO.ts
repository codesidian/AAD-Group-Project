import * as Types from "./Types";
import * as Config from "../config";

const items: Map<string, Types.Item> = new Map<string, Types.Item>([
    ["ethanol", {code: "ethanol", name:"Ethanol", price:100, quantity: 1, is_chemical: true, pack_size: 1, for_sale: true}],
    ["pencil", {code: "pencil", name:"Pencil", price:10, quantity: 1, is_chemical: false, pack_size: 1, for_sale: true}],
    ["pen", {code: "pen", name:"Pen", price:25, quantity: 1, is_chemical: false, pack_size: 1, for_sale: true}],
]);

export default class RemoteDAO implements Types.StoresDAO {
    getVersion(): Promise<string> {
        return new Promise<string>(res => res(Config.APP_VERSION));
    }

    async getItem(itemCode: string): Promise<Types.Item> {
        const response = await fetch(`http://localhost:8000/api/items/${itemCode}/`, {
            method: "GET",
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin'
        })

        if (response.status === 404) {
            throw Error("Invalid item");
        }

        const item = await response.json();
        if (Types.isItem(item)) {
            return item;
        } else {
            throw Error("Unexpected error retriving item");
        }
    }

    checkout(items: ArrayLike<Types.SaleItem>): Promise<Types.Sale> {
        return new Promise<Types.Sale>((res, rej) => {
            let sale: Types.Sale = {items: items, sale_id: 1234};
            res(sale);
        });
    }
}
