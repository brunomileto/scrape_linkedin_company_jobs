from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from linkedin_crawler.utils import linkeding_utils

class CompanyJobsSpider(Spider):
    name = 'company_jobs'
    allowed_domains = ['linkedin.com', 'google.com']
    number_of_pages = 0

    def start_requests(self):
        
        company_jobs = self.navigate_to_company_jobs()
        'disabled.ember-view.job-card-container__link job-card-list__title'
        page = Selector(text=self.driver.page_source)
        jobs = page.xpath('//*[contains(@class, "disabled ember-view job-card-container__link job-card-list__title")]/@href').extract()
        for job in jobs:
            job_full_url = 'https://linkedin.com' + job
            yield Request(job_full_url, callback=self.parse_job)
        
        while True:
            current_url = self.driver.current_url
            if current_url[len(current_url)-8:].find('start') >= 0:
                url_number = int(current_url[len(current_url)-2:])+25
                next_url = current_url[:len(current_url)-2] + url_number

            else:
                next_url = current_url + '&start=25'
            
            self.driver.get(next_url)
            sleep(4)
            try:
                last_page = self.driver.find_element_by_class_name('t-24.t-black.t-normal.mb5.mt5.text-align-center')
                last_page.get_attribute('innerHTML')
                if last_page == 'Nenhuma vaga corresponde aos seus critérios':
                    self.logger_info('NO MORE PAGES TO LOAD !!!!!!!!!!!!!!!!')
                    self.driver.quit()
                    break
            except NoSuchElementException:
                self.logger_info('NOT THE LAST PAGE')
                page = Selector(text=self.driver.page_source)
                jobs = page.xpath('//*[contains(@class, "disabled ember-view job-card-container__link job-card-list__title")]/@href').extract()
                for job in jobs:
                    job_full_url = 'https://linkedin.com' + job
                    yield Request(job_full_url, callback=self.parse_job)

    def navigate_to_company_jobs(self):
        options = Options()
        options.add_argument("window-size=990,900")
        executable_path = 'C:\selenium_drivers\chromedriver'
        self.driver = webdriver.Chrome(options=options, executable_path=executable_path)

        linkeding_utils.linkedin_login(self.driver, 'bruno_mileto@outlook.com', 'miletominarlz1')
        linkeding_utils.find_company_in_google(self.driver, ['DeepIntent', 'Broadway', 'New York', 'linkedin'])
        linkeding_utils.from_company_page_go_to_its_jobs(self.driver)
        linkeding_utils.page_down(self.driver, 'body')
        linkeding_utils.page_up(self.driver, 'body')
        return self.driver.find_elements_by_class_name('artdeco-entity-lockup__subtitle.ember-view')

    def parse_job(self, response):
        job_page = Selector(text=self.driver.page_source)
        job_url = self.driver.current_url
        job_title = job_page.xpath('//*[@class="t-24.t-bold"]/text()').extract_first()
        test = job_page.xpath('//*[@class="p5"]/h1/text')
        # self.go_to_job_page(job=job)
        # #scrape
        # self.back_to_jobs_list()
        # linkeding_utils.page_down(self.driver, self.driver.find_element_by_tag_name('body'))
        # linkeding_utils.page_up(self.driver, self.driver.find_element_by_tag_name('body'))
        pass
    # def go_to_job_page(self, job):
    #     self.driver.execute_script("arguments[0].click();", job)
    #     sleep(5)
    #     return

    # def back_to_jobs_list(self):
    #     driver.execute_script("window.history.go(-1)")
    #     sleep(5)  
    #     return   

    # def page_down(self):
    #     times = 20
    #     jobs_page = driver.find_element_by_tag_name('body')
    #     while times > 0:
    #         jobs_page.send_keys(Keys.PAGE_DOWN)
    #         times -= 1
    #     return

    # def page_up(self):
    #     times = 20
    #     jobs_page = driver.find_element_by_tag_name('body')
    #     while times > 0:
    #         jobs_page.send_keys(Keys.PAGE_UP)
    #         times -= 1
    #     return

    # def linkedin_login(self):
    #     self.driver.get('https://www.linkedin.com')
    #     username = self.driver.find_element_by_name('session_key')
    #     username.send_keys('bruno_mileto@outlook.com')
    #     sleep(3)
    #     password = self.driver.find_element_by_name('session_password')
    #     password.send_keys('miletominarlz1')
    #     sleep(3)
    #     sign_in_button = self.driver.find_element_by_class_name('sign-in-form__submit-button')
    #     sign_in_button.click()
    #     sleep(10)
    #     return

    # def find_company_page(self):
    #     self.driver.get('https://google.com/')
    #     search_query = self.driver.find_element_by_name('q')
    #     search_query.send_keys('"DeepIntent" "Broadway" "New York" "linkedin"')
    #     search_query.send_keys(Keys.RETURN)
    #     sleep(3)
    #     url = self.driver.find_element_by_xpath('//*[@id="rso"]/div/div[1]/div/div/div[1]/a/h3')
    #     url.click()
    #     sleep(4)
    #     return

    # def go_to_company_jobs(self):
    #     self.driver.find_elements_by_xpath('/html/body/div[7]/div[3]/div/div/div/div[2]/main/div[1]/section/div/div[2]/div[2]/nav/ul/li[4]/a').click()
    #     sleep(3)
    #     self.driver.find_elements_by_xpath('/html/body/div[7]/div[3]/div/div/div/div[2]/main/div[2]/div/div[2]/div/a').click()
    #     sleep(3)
    #     return


