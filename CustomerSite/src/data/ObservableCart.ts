import Cart from "./Cart";
import { Item, SaleItem } from "./Types";

export type CartObserver = (updated: ObservableCart) => void;

export default class ObservableCart implements Cart {
    observers = new Array<CartObserver | undefined>();

    constructor(public backingCart: Cart) {
    }

    addItem = (item: Item): void => {
        this.backingCart.addItem(item);
        this.invokeObservers();
    }
    
    getItems = (): ArrayLike<SaleItem> => {
        return this.backingCart.getItems();
    }

    setItemQuantity = (code: string, quantity: number): void => {
        this.backingCart.setItemQuantity(code, quantity);
        this.invokeObservers();
    }

    clear = () => {
        this.backingCart.clear();
        this.invokeObservers();
    }

    invokeObservers = () => {
        this.observers.forEach(observer => {
            if (observer !== undefined) {
                observer(this);
            }
        });
    }

    addObserver = (observer: CartObserver): number => {
        return this.observers.push(observer) - 1;
    }

    removeObsever = (handle: number) => {
        this.observers[handle] = undefined;
    }
}