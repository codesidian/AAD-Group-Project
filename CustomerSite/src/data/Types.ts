export interface StoresDAO {
    getVersion(): Promise<string>;
    getItem(itemCode: string): Promise<Item>;
    checkout(items: ArrayLike<SaleItem>): Promise<Sale>;
};

export type Item = {
    code: string;
    name: string;
    price: number;
    quantity: number;
    is_chemical: boolean;
    pack_size: number;
    for_sale: boolean;
};

export type SaleItem = {
    item: Item;
    quantity: number;
};

export type Sale = {
    sale_id: number;
    items: ArrayLike<SaleItem>;
};

export function isItem(obj: any): obj is Item {
    let item = obj as Item;
    return item.code !== undefined && item.name != undefined;
}

export function isSaleItem(obj: any): obj is SaleItem {
    let item = obj as SaleItem;
    return item.quantity !== undefined;
}

export function isSale(obj: any): obj is Sale {
    let sale = obj as Sale;
    return sale.sale_id !== undefined && sale.items !== undefined;
}