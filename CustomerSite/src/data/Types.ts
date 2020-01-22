export interface StoresDAO {
    getVersion(): string;
    getItem(itemCode:string): Item | undefined;
};

export type Item = {
    itemCode: string;
    name: string;
    price: number;
    quantity: number;
    isChemical: boolean;
    packSize: number;
    forSale: boolean;
};

export function isItem(obj: any): obj is Item {
    let item = obj as Item;
    return item.itemCode !== undefined && item.name != undefined;
}

