let logger = console

export class DeviceAdatper {
    objIndex: number = 0;

    callUiTest(api: string, thisRef: string, ...params: any[]): string {
        this.objIndex += 1;
        logger.info(`api [${api}], this [${thisRef}], params ${params}, return ${this.objIndex}`);
        return this.objIndex.toString()
    }

    callUiTestObjects(api: string, thisRef: string, ...params: any[]): string[] {
        let arr = new Array()
        this.objIndex += 1;
        for (var i = 0; i < 10; i++) {
            arr.push(this.objIndex.toString())
            this.objIndex += 1;
        }
        logger.info(`api [${api}], this [${thisRef}], params ${params}, return ${arr}`);
        return arr;
    }

    connect(deviceSn: string) {
        logger.info(`connect to ${deviceSn}`);
    }

    disconnect() {
        logger.info("disconnect")
    }
}