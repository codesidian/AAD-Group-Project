import * as Types from "./Types";

export default interface Cart {
    addItem(item: Types.Item): void;
    getItems(): ArrayLike<Types.SaleItem>;
    setItemQuantity(code: string, quantity: number): void;
    clear(): void;
}
