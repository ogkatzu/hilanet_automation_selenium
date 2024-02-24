from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import random
import datetime


def read_credentials(filename):
    credentials = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split(' = ')
            credentials[key] = value
    return credentials


current_day = datetime.datetime.now().weekday()

if __name__ == "__main__":
    if 0 <= current_day <= 3:
        filename = "details.txt"
        cred = read_credentials(filename=filename)
        username = str(cred.get("USERNAME"))
        try:
            # options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            dr = webdriver.Chrome()
            dr.get("https://infinidat.net.hilan.co.il/login")
            user_name = dr.find_element(by="id", value="user_nm")
            user_name.send_keys(username)
            password = dr.find_element(by="id", value="password_nm")
            password.send_keys(str(cred.get("PASSWORD")))
            sleep(10)
            dr.find_element(by="xpath", value=r'//*[@id="mainViewPlaceholder"]/div/div/div[6]/button').click()
            sleep(10)
            dr.find_element(by="xpath", value="/html/body/h-root/h-main-layout/div[2]/h-home/h-app-component"
                                              "-layout/div[2]/div/div[1]/div/div/div[2]/div[3]"
                                              "/h-display-attendance[1]/div/div/div[2]/div[2]/button[1]").click()
            sleep(10)
            start_time = dr.find_element(by="id", value="ctl00_mp_RG_Days_91121743_2024_02_cellOf_ManualEntry_"
                                                        "EmployeeReports_row_0_0_ManualEntry_EmployeeReports_row_0_0")
            minutes = str(random.randint(1, 9))
            full_start_time = "09:0" + minutes
            dr.execute_script("arguments[0].value = arguments[1] + arguments[0].value;",
                              start_time, full_start_time)
            # start_time.send_keys("00")
            # start_time.send_keys("00")
            end_time = dr.find_element(by="id", value="ctl00_mp_RG_Days_91121743_2024_02_cellOf_"
                                                      "ManualExit_EmployeeReports_row_0_0_ManualExit_"
                                                      "EmployeeReports_row_0_0")
            minutes = str(random.randint(35, 55))
            full_end_time = "17:" + minutes
            dr.execute_script("arguments[0].value = arguments[1] + arguments[0].value;", end_time, full_end_time)
            dropdown = Select(dr.find_element(by="id", value="ctl00_mp_RG_Days_91121743_2024_02_cellOf_Symbol.SymbolId_"
                                                             "EmployeeReports_row_0_0_Symbol.SymbolId_"
                                                             "EmployeeReports_row_0_0"))
            dropdown.select_by_visible_text("נוכחות")
            hours = dr.find_element(by="xpath", value='//*[@id="calendar_container"]'
                                                      '/tbody/tr[4]/td[4]/table/tbody/tr[2]/td')
            print(hours.text)
            sleep(5)
            submit_button = dr.find_element(by="xpath", value='//*[@id="ctl00_mp_RG_Days_91121743_2024_02_btnSave"]')
            submit_button.click()
            sleep(10)
        finally:
            dr.quit()
    else:
        current_day = datetime.datetime.now().strftime("%A")
        print(f"Today is {current_day}, and this script cannot run on the weekend")
        