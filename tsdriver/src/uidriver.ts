import { By } from "./by";
import { RemoteObject } from "./rpc/remoteObject";
import { Resolver } from "./rpc/remoteObject";
import { DeviceAdatper } from "./rpc/rpcClient";
import { UiComponent } from "./uicomponent";


export class UiDriver extends RemoteObject {

    static connect(deviceSn: String): UiDriver {
        let rpcClient = new DeviceAdatper()
        let resolver: Resolver = {
            toString(): string {
                return "Driver#" + deviceSn
            },

            resolve(rpcClient): string {
                return rpcClient.callUiTest("Driver.create", "", deviceSn);
            }
        }
        return new UiDriver(resolver, rpcClient);
    }

    findComponent(by: By): UiComponent {
        let thisDriver = this;
        let resolver: Resolver = {
            toString(): string {
                return "Component#" + by.toString()
            },

            resolve(rpcClient): string {
                return rpcClient.callUiTest("Driver.findComponent", thisDriver, by.getRemoteRef());
            }
        }
        return new UiComponent(resolver, this.getRpcClient());
    }

    findComponents(by: By): UiComponent[] {
        let refs = ["UiComponent#1", "UiComponent#2"];
        let results = new Array();
        let thisDriver = this;
        for (let i = 0; i < refs.length; i++) {
            let resolver = {
                toString(): string {
                    return `Component#${by.toString()}#index_${i}`;
                },
                resolve(rpcClient: any): string {
                    results = rpcClient.callUiTestObjects("Driver.findComponents", thisDriver, by.getRemoteRef());
                    return results[i];
                }
            }
            results.push(new UiComponent(resolver, this.getRpcClient()));
        }
        return results;
    }

    by(): By {
        return By.seed(this.getRpcClient());
    }
}