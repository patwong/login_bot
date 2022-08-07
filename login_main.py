# simple login bot using firefox
# requires login, confirmation webpage, and logout url stored in yamjam

from datetime import datetime
from YamJam import yamjam
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

user_info = yamjam()['login_bot']
ff_profile_location = user_info['ff_profile']
firefox_profile = webdriver.FirefoxProfile(ff_profile_location)
ff_extensions = user_info['extensions']
username_list = user_info['username_list']
password_list = user_info['password']
login_url = user_info['login_url']
login_menu = user_info['login_menu']
login_user_element = user_info['login_user_element']
login_pw_element = user_info['login_pw_element']
login_button_element = user_info['login_button']
logged_in_page = user_info['logged_in_page']
login_check1 = user_info['confirm_element1']
login_check2 = user_info['confirm_element2']
logout_button = user_info['logout_button']
hover_menu_id = user_info['hover_menu']

output_string = ""
output_temp = ""

# browser driver
browser = webdriver.Firefox(firefox_profile)

# check if extension is singular string or a list
if type(ff_extensions) is list:
    for extension in ff_extensions:
        browser.install_addon(extension, temporary=True)
    # loop
elif type(ff_extensions) is str:
    browser.install_addon(ff_extensions, temporary=True)
else:
    import sys
    sys.exit('bad extension')
# end

# login loop
for user in username_list:
    # try:
    browser.get((login_url))
    xpath_create = '//a[contains(@href,'+ '"'+ login_menu + '"' + ')]'
    login_button = browser.find_element_by_xpath(xpath_create)
    login_button.click()
    username = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.ID, login_user_element)))
    username.send_keys(user)
    password = browser.find_element_by_id(login_pw_element)
    password.send_keys(password_list[username_list[user]])
    login_button = browser.find_element_by_id(login_button_element)
    login_button.click()

    # confirming user has logged in
    element_locate = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, login_check1)))
    # visiting a webpage after logging in and confirming an element exists
    browser.get(logged_in_page)
    element_locate = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, login_check2)))

    # logout and wait
    browser.implicitly_wait(20)
    xpath_create = "//*[contains(text()," + "'" + logout_button + "'" + ")]"
    hover_menu = ActionChains(browser)
    hover_find = browser.find_element(By.CLASS_NAME, hover_menu_id)
    hover_menu.move_to_element(hover_find).perform()
    logout_now = browser.find_element(By.XPATH,xpath_create)
    logout_now.click()
    browser.implicitly_wait(20)
    
    # adding timestamp and username to log upon successful login/logout
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_datetime = '[' + current_datetime + ']'
    output_temp = current_datetime + " user logged in/out: " + user
    print(output_temp)
    output_string += output_temp + '\n'
    # except:
        # import sys
        # sys.exit('something went wrong')
# end loop
browser.quit()

# write out to log
# log's filename created to not interfere with cmd tab autocomplete and
# to differentiate with update log
with open('bot_log.log', 'a') as output_file:
   output_file.write(output_string)
# end with

