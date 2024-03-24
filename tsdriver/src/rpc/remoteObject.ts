import { DeviceAdatper } from "./rpcClient";
let logger = console


const objectCallbackMap = new WeakMap<object, () => void>();

function createObjectWithCallback(callback: () => void) {
  const object = {
    // ...对象的属性和方法
  };
  objectCallbackMap.set(object, callback);

  return object;
}

const myObject = createObjectWithCallback(() => {
  console.log('Object is garbage collected');
});


export interface Resolver {

    /**
     * 返回远程引用
     */
    resolve(rpcClient: any): string;
    toString(): string;

}

export class RemoteObject {
    remoteRef: string;
    rpcClient: DeviceAdatper;
    resolver: Resolver;

    constructor(resolver: Resolver, rpcClient: DeviceAdatper) {
        this.resolver = resolver;
        this.rpcClient = rpcClient;
        this.remoteRef = "";
        let destructor = () => {this.release()}
        destructor.bind(this);
        objectCallbackMap.set(this, destructor);
    }

    getRemoteRef() {
        return this.resolve();
    }

    getRpcClient() {
        return this.rpcClient;
    }

    resolve() {
        if (!this.isResolved()) {
            logger.info(`start to resolve ${this.resolver}`);
            this.remoteRef = this.resolver.resolve(this.getRpcClient())
            if (!this.isResolved()) {
                throw `Fail to resolve object [${this.resolver.toString()}]`
            }
            logger.info(`resolve result [${this.remoteRef}]`)
        }
        return this.remoteRef
    }

    isResolved() {
        if (this.remoteRef) {
            return true;
        } else {
            return false;
        }
    }
    
    release() {
        if (this.isResolved()) {
            let tmpRef = this.remoteRef;
            this.remoteRef = "";
            return tmpRef;
        }
        return ""
    }
    
    toString(): string {
        return this.resolver.toString();
    }
}