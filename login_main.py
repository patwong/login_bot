# simple login bot using firefox
# requires login, confirmation webpage, and logout url stored in yamjam

from datetime import datetime
from YamJam import yamjam
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_info = yamjam()['login_bot']
ff_profile_location = user_info['ff_profile']
firefox_profile = webdriver.FirefoxProfile(ff_profile_location)
ff_extensions = user_info['extensions']
username_list = user_info['username_list']
master_password = user_info['password']
login_url = user_info['login_url']
login_user_element = user_info['login_user_element']
login_pw_element = user_info['login_pw_element']
login_button_element = user_info['login_button']
logged_in_page = user_info['logged_in_page']
login_check1 = user_info['confirm_element1']
login_check2 = user_info['confirm_element2']
logout_url = user_info['logout_url']
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
    try:
        browser.get((login_url))
        username = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, login_user_element)))
        username.send_keys(user)
        password = browser.find_element_by_id(login_pw_element)
        password.send_keys(master_password)
        login_button = browser.find_element_by_id(login_button_element)
        login_button.click()

        # confirming user has logged in
        element_locate = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, login_check1)))
        # visiting a webpage after logging in and confirming an element exists
        browser.get(logged_in_page)
        element_locate = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, login_check2)))

        # logout and wait
        browser.implicitly_wait(20)
        browser.get(logout_url)
        browser.implicitly_wait(20)
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_datetime = '[' + current_datetime + ']'
        output_temp = current_datetime + " user logged in/out: " + user
        print(output_temp)
        output_string += output_temp + '\n'
    except:
        import sys
        sys.exit('something went wrong')
# end loop
browser.quit()

# write out to log
# log's filename created to not interfere with cmd tab autocomplete and
# to differentiate with update log
with open('bot_log.log', 'a') as output_file:
    output_file.write(output_string)
# end with

