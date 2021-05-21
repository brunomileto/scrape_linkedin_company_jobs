from time import sleep
from selenium.webdriver.common.keys import Keys

def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)
    sleep(5)
    return

def back_one_page(driver):
    driver.execute_script("window.history.go(-1)")
    sleep(5)  
    return   

def page_down(driver, element):
    times = 20
    page = driver.find_element_by_tag_name(element)
    while times > 0:
        page.send_keys(Keys.PAGE_DOWN)
        times -= 1
    return

def page_up(driver, element):
    times = 20
    page = driver.find_element_by_tag_name(element)
    while times > 0:
        page.send_keys(Keys.PAGE_UP)
        times -= 1
    return

def linkedin_login(driver, username, password):
    driver.get('https://www.linkedin.com')
    username = driver.find_element_by_name('session_key')
    username.send_keys('bruno_mileto@outlook.com')#'bruno_mileto@outlook.com'
    sleep(3)
    password = driver.find_element_by_name('session_password')
    password.send_keys('miletominarlz1')#'miletominarlz1'
    sleep(3)
    sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
    sign_in_button.click()
    sleep(10)
    return

def from_company_page_go_to_its_jobs(driver):
    ul = driver.find_element_by_class_name('org-page-navigation__items')
    lis = ul.find_elements_by_tag_name('li')[3].click()
    sleep(3)       
    driver.find_element_by_class_name('link-without-hover-visited.mt5.ember-view').click()
    sleep(3)
    return 

def find_company_in_google(driver, search_queries_list):
    driver.get('https://google.com/')
    search_query = driver.find_element_by_name('q')
    search_query.send_keys(', '.join([f'"{query}"' for query in search_queries_list]))#'"DeepIntent" "Broadway" "New York" "linkedin"')
    search_query.send_keys(Keys.RETURN)
    sleep(3)
    url = driver.find_element_by_xpath('//*[@id="rso"]/div/div[1]/div/div/div[1]/a/h3')
    url.click()
    sleep(4)
    return


