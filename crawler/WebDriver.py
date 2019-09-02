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

    # core

    def _click_xpath_element(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()

    def _send_keys_xpath_element(self, xpath, keys):
        self.driver.find_element_by_xpath(xpath).send_keys(keys)

    def _switch_frame_to(self, xpath, is_parent=None) -> None:
        if is_parent:
            self.driver.switch_to.parent_frame()
            return
        self.driver.switch_to.frame(self.driver.find_element_by_xpath(xpath))

    # logic

    def _get_page_from_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(1)

    def _login(self, id, pw):
        self._send_keys_xpath_element('// *[ @ id = "id"]', id)
        self._send_keys_xpath_element('// *[ @ id = "password"]', pw)
        self._click_xpath_element('// *[ @ id = "logbtn"]')
        self.driver.implicitly_wait(1)

    def _logic_go_to_riaframe(self):
        # 컨텐츠 frame 으로 이동
        self._switch_frame_to('// *[ @ id = "contentFrm"]')
        # 수강신청내역 frame 으로 이동
        self._switch_frame_to('// *[ @ id = "riaframe"]')

    def _logic_move_to_sugang(self):
        # 매뉴 frame 으로 switch
        self._switch_frame_to('// *[ @ id = "menuFrm"]')
        # 수업/성적 클릭
        self._click_xpath_element('//*[@id="mainTable"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr[3]')
        # 강좌조회 및 수강신청 클릭
        self._click_xpath_element('// *[ @ id = "SELF_STUDSELF_SUB_30"] / table / tbody / tr[1] / td')
        # 수강내용조회/출력 클릭
        self._click_xpath_element('// *[ @ id = "SELF_STUDSELF_SUB_30SELF_MENU_10"] / table / tbody / tr[4]')

        # 수강내용조회/출력 컨텐츠 frame 으로 switch
        # https://stackoverflow.com/questions/17856187/how-to-navigate-back-to-current-page-from-frame-in-selenium-webdriver
        self.driver.implicitly_wait(1)
        # 부모 frame 으로 이동
        self._switch_frame_to(None, is_parent=True)
        # 수강신청내역 frame 으로 이동
        self._logic_go_to_riaframe()
        # 수강신청 페이지 Next 버튼 클릭
        self._click_xpath_element('//*[@id="btnNext"]')

        # 교과목명 검색 -> 검색어 입력
        set_search = input("검색 설정 완료(Y) : ")
        # 검색 버튼 클릭
        # 일단 수동으로 하자
        # if set_search == 'Y':
        #     self._click_xpath_element('//*[@id="btnDivSearch"]')

    def _logic_sugang_cycle(self):

        main_window = self.driver.window_handles[0]

    def _logic_cycle_01(self):
        """
        수강내역에 의견등록을 수행하는 사이클
        window 는 사이클 함수내에서 관리한다. (self 로 멤버변수로 저장하지 않음)
        한번 사이클이 돌면 바로 다음 사이클이 돌 수 있도록 frame 변경함
        :return:
        """

        # 메인(uis) 페이지 윈도우 저장
        main_window = self.driver.window_handles[0]
        # 의견등록 클릭
        self._click_xpath_element(
            '// *[ @ id = "rpt"] / tbody / tr[2] / td / div / div[1] / table / tbody / tr[2] / td[9] / button')

        # 의견등록 window 로 switch
        # https://stackoverflow.com/questions/10629815/how-to-switch-to-new-window-in-selenium-for-python
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)
        self._click_xpath_element('//*[@id="guide"]')
        self._click_xpath_element('//*[@id="container"]/div/div/div[2]/div/div[2]/a/span/img')
        self._click_xpath_element('//*[@id="guide"]')
        self._send_keys_xpath_element('//*[@id="tx_editor_form"]/div/table/tbody/tr[1]/td/div/div/ul/li/input', '제목')
        # 저장(submit)은 구현하지 않음.

        # 메인 window 로 switch
        self.driver.implicitly_wait(1)
        current_window = self.driver.current_window_handle  # == new_window
        self.driver.window_handles.remove(current_window)
        self.driver.close()
        self.driver.switch_to.window(main_window)
        # print(self.driver.page_source)
        # 다시 메인 window 로 넘어오면 default frame 으로 switch 되어있다.
        # 다시 원하는 frame 으로 switch 해야함

        # 수강신청내역 frame 으로 이동
        self._logic_go_to_riaframe()

    # entry

    def start(self) -> bool:
        # page 접근
        self._get_page_from_url('https://portal.sejong.ac.kr/jsp/login/uisloginSSL.jsp')

        # 로그인
        self._login(config.id, config.pw)

        # 수강신청 사이클은 이 아래 코드를 변경

        # start cycle
        # 수강내용조회/출력 으로 이동
        self._logic_move_to_sugang()

        # self._logic_cycle_01()
        # self._logic_cycle_01()
        # self._logic_cycle_01()

        return True
