import * as Types from "./Types";
import * as Config from "../config";
import Cookies from 'js-cookie';

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
        const response = await fetch(`/api/items/${itemCode}/`, {
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

    async checkout(items: ArrayLike<Types.SaleItem>): Promise<Types.Sale> {
        let body = {"items": Array.from(items).map(x => ({"code": x.item.code, "quantity": x.quantity}))};

        const csrfToken = Cookies.get('csrftoken');
        if (csrfToken == undefined) {
            throw Error("No CSRF token");
        }
        
        const response = await fetch('/api/sales/make/', {
            method:"PUT",
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {'X-CSRFToken': csrfToken, "Content-Type": "application/json"},
            body: JSON.stringify(body)
        });

        if (response.status !== 200) {
            throw Error("Unexpected error processing purchase");
        }

        const sale = await response.json();
        if (Types.isSale(sale)) {
            for (let i = 0; i < sale.saleitem_set.length; i++) {
                // api returns string, we need item
                let itemId = (sale.saleitem_set[i].item as unknown as string);
                for (let j = 0; j < items.length; j++) {
                    if (itemId === items[j].item.code) {
                        sale.saleitem_set[i].item = items[j].item;
                        break;
                    }
                }
            }
            return sale;
        } else {
            throw Error("Unexpected error decoding sale");
        }
    }
}
