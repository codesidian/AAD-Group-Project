import * as Types from "./Types";
import * as Config from "../config";

const items: Map<string, Types.Item> = new Map<string, Types.Item>([
    ["ethanol", {code: "ethanol", name:"Ethanol", price:100, quantity: 1, is_chemical: true, pack_size: 1, for_sale: true}],
]);

export default class TestDAO implements Types.StoresDAO {
    getVersion(): Promise<string> {
        return new Promise<string>(res => res(Config.APP_VERSION));
    }

    getItem(itemCode: string): Promise<Types.Item> {
        return new Promise<Types.Item>((res, rej) => {
            const item = items.get(itemCode);
            if (item === undefined) {
                rej("Invalid item")
            } else {
                //res(item);
                setTimeout(() => res(item), 500);
            }
        });
    }
}
