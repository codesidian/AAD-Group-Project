import Cart from "./Cart";
import { Item, SaleItem } from "./Types";

export default class MemoryCart implements Cart {
    items = new Array<SaleItem>();

    addItem(item: Item): void {
        let saleItem = this.items.find(x => x.item.code === item.code);
        if (saleItem === undefined) {
            saleItem = {item: item, quantity: 0};
            this.items.push(saleItem);
        }
        saleItem.quantity++;
    }

    getItems(): ArrayLike<SaleItem> {
        return this.items;
    }

    setItemQuantity(code: string, quantity: number): void {
        let saleItem = this.items.find(x => x.item.code === code);
        if (saleItem === undefined) {
            throw new Error("Sale item not found");
        }
        if (quantity <= 0) {
            this.items.splice(this.items.indexOf(saleItem), 1);
        } else {
            saleItem.quantity = quantity;
        }
    }

    clear(): void {
        this.items = new Array<SaleItem>();
    }
}
