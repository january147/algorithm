import { UiDriver } from "./src/uidriver";

let driver: UiDriver = UiDriver.connect("aaaaaa")
driver.findComponent(driver.by().text("haha").isBefore(driver.by().text("hehe"))).click()

driver.findComponents(driver.by().text("haha"))[1].click()

