import { RemoteObject, Resolver } from "./rpc/remoteObject";
import { DeviceAdatper } from "./rpc/rpcClient";

export class By extends RemoteObject{

    static seed(rpcClient: DeviceAdatper) {
        let resolver: Resolver = {
            resolve(rpcClient) {
                return "On#seed";
            },
            toString() {
                return "On#seed";
            }
        }
        return new By(resolver, rpcClient);
    }

    text(text: string) {
        let resolve_func = (rpcClient: DeviceAdatper) => {
            return rpcClient.callUiTest("On.text", this.getRemoteRef(), text);
        }
        resolve_func.bind(this);
        let resolver: Resolver = {
            resolve: resolve_func,
            toString() {
                return `text(${text})`;
            }
        }
        return new By(resolver, this.rpcClient);

    }

    isBefore(anchor: By) {
        let resolve_func = (rpcClient: DeviceAdatper) => {
            return rpcClient.callUiTest("On.isBefore", this.getRemoteRef(), anchor.getRemoteRef());
        }
        resolve_func.bind(this);
        let resolver: Resolver = {
            resolve: resolve_func,
            toString() {
                return anchor.toString();
            }
        }
        return new By(resolver, this.rpcClient);
    }
}