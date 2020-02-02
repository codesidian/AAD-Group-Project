export interface StoresDAO {
    getVersion(): Promise<string>;
    getItem(itemCode:string): Promise<Item>;
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

export function isItem(obj: any): obj is Item {
    let item = obj as Item;
    return item.code !== undefined && item.name != undefined;
}

