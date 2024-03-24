import { RemoteObject } from "./rpc/remoteObject";
import { DeviceAdatper } from "./rpc/rpcClient";

export class UiComponent extends RemoteObject {

    click() {
        this.rpcClient.callUiTest("Component.click", this.getRemoteRef())
    }
}