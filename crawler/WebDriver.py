from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import config


class HeadLessChrome:

    def __init__(self, driver_path='C:/chromedriver_win32/chromedriver'):
        self.driver_path = driver_path
        options = webdriver.ChromeOptions()
        # options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        # options.add_argument('headless')
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=options)
        self.driver.implicitly_wait(1)

    def start(self) -> bool:
        """

        :return: success
        """
        # page 접근
        self.driver.get('https://portal.sejong.ac.kr/jsp/login/uisloginSSL.jsp')
        self.driver.implicitly_wait(1)

        # 로그인
        self.driver.find_element_by_xpath('// *[ @ id = "id"]').send_keys(config.id)
        self.driver.find_element_by_xpath('// *[ @ id = "password"]').send_keys(config.pw)
        self.driver.find_element_by_xpath('// *[ @ id = "logbtn"]').click()

        # 매뉴 frame 으로 switch
        self.driver.implicitly_wait(1)
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('// *[ @ id = "menuFrm"]'))
        # 수업/성적 클릭
        self.driver.find_element_by_xpath(
            '//*[@id="mainTable"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr[3]').click()
        # 강좌조회 및 수강신청 클릭
        self.driver.find_element_by_xpath('// *[ @ id = "SELF_STUDSELF_SUB_30"] / table / tbody / tr[1] / td').click()
        # 수강내용조회/출력 클릭
        self.driver.find_element_by_xpath(
            '// *[ @ id = "SELF_STUDSELF_SUB_30SELF_MENU_10"] / table / tbody / tr[5]').click()

        # 수강내용조회/출력 컨텐츠 frame 으로 switch
        # https://stackoverflow.com/questions/17856187/how-to-navigate-back-to-current-page-from-frame-in-selenium-webdriver
        self.driver.implicitly_wait(1)
        self.driver.switch_to.parent_frame()  # 부모 frame 으로 이동
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('// *[ @ id = "contentFrm"]'))  # 컨텐츠 frame 으로 이동
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('// *[ @ id = "riaframe"]'))  # 수강신청내역 frame 으로 이동
        # 의견등록 클릭
        main_window = self.driver.window_handles[0]
        self.driver.find_element_by_xpath(
            '// *[ @ id = "rpt"] / tbody / tr[2] / td / div / div[1] / table / tbody / tr[2] / td[9] / button').click()

        # 의견등록 window 로 switch
        # https://stackoverflow.com/questions/10629815/how-to-switch-to-new-window-in-selenium-for-python
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)
        self.driver.find_element_by_xpath('//*[@id="guide"]').click()
        self.driver.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/div/div[2]/a/span/img').click()
        self.driver.find_element_by_xpath('//*[@id="guide"]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="tx_editor_form"]/div/table/tbody/tr[1]/td/div/div/ul/li/input').send_keys('제목')
        # 저장(submit)은 구현하지 않음.

        # 메인 window 로 switch
        self.driver.implicitly_wait(1)
        current_window = self.driver.current_window_handle  # == new_window
        self.driver.window_handles.remove(current_window)
        self.driver.close()
        self.driver.switch_to.window(main_window)
        # print(self.driver.page_source)
        # 다시 메인 window 로 넘어오면 default 로 switch 되어있다.
        # 다시 원하는 frame 으로 switch 해야함

        # 반복 작업 (Loop 가능)
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('// *[ @ id = "contentFrm"]'))  # 컨텐츠 frame 으로 이동
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('// *[ @ id = "riaframe"]'))  # 수강신청내역 frame 으로 이동
        self.driver.find_element_by_xpath(
            '// *[ @ id = "rpt"] / tbody / tr[2] / td / div / div[1] / table / tbody / tr[2] / td[9] / button').click()
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)
        self.driver.find_element_by_xpath('//*[@id="guide"]').click()
        self.driver.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/div/div[2]/a/span/img').click()
        self.driver.find_element_by_xpath('//*[@id="guide"]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="tx_editor_form"]/div/table/tbody/tr[1]/td/div/div/ul/li/input').send_keys('제목')

        return True
