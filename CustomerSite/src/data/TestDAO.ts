import * as Types from "./Types";
import * as Config from "../config";

const items: Map<string, Types.Item> = new Map<string, Types.Item>([
    ["ethanol", {itemCode: "ethanol", name:"Ethanol", price:100, quantity: 1, isChemical: true, packSize: 1, forSale: true}],
]);

export default class TestDAO implements Types.StoresDAO {
    getVersion(): string {
        return Config.APP_VERSION;
    }

    getItem(itemCode: string): Types.Item | undefined {
        return items.get(itemCode);
    }
}
