from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import csv
import os

IS_DEBUG = True

class TitleLink:
    def __init__(self, title, link):
        self.title = title
        self.link = link

def write_to_csv(csv_file_path,data):
    with open(csv_file_path, 'a', encoding='utf-8',newline='') as file:
        writer = csv.writer(file)
        if os.path.exists(csv_file_path) and os.stat(csv_file_path).st_size == 0: #Check if contains any content
            print("file doesnt exists")
            writer.writerow(["Department", "Role", "Prompt","PromptText"])  # Write header row
        # print(data)
        writer.writerows(data)        
    print("Written "+data[0][2]+"\n")

def get_department_links(driver):
    department_title = ""
    department_link = ""
    department_data = []
    department_xpath = "//a[contains(@class, 'bnnr-elmntbx-wrap') and contains(@class, 'elemntbx_main') and contains(@class, 'w-inline-block')]"
    department_title_xpath = "//p[@class='elmnt-txt mainelmnt_txt match_height']"
    department_selector =  wait.until(EC.presence_of_all_elements_located((By.XPATH,department_xpath)))
    for department in department_selector:
        department_link = department.get_attribute("href")
        title_elements = department.find_elements(By.XPATH, department_title_xpath)
        title = title_elements[0].get_attribute("innerHTML")
        for title in title_elements:
            department_title = title.get_attribute("innerHTML")
            break
        department_data.append(TitleLink(department_title,department_link))
        if IS_DEBUG:
            break
    for department in department_data:
        for role in get_roles_links(department.link,driver):
            for prompt in get_prompts_links(role.link,driver):
                
                
                prompt_content = get_prompts_content(prompt.link,driver)
                # print(prompt_content)
                for_csv = []
                for_csv.append([department.title,role.title,prompt.title,prompt_content])
                
                write_to_csv("lol.csv",for_csv)

def get_roles_links(url,driver):
    driver.get(url)
    role_data = []
    role_title = ""
    role_link = ""
    wait.until(EC.url_to_be(url))
    role_xpath = "//a[contains(@class, 'bnnr-elmntbx-wrap') and contains(@class, 'elemntbx_main') and contains(@class, 'w-inline-block')]"
    role_title_xpath = "//p[@class='elmnt-txt mainelmnt_txt match_height']"

    role_selector =  wait.until(EC.presence_of_all_elements_located((By.XPATH,role_xpath)))
    for role in role_selector:
        role_link = role.get_attribute("href")
        title_elements = role.find_elements(By.XPATH, role_title_xpath)
        title = title_elements[0].get_attribute("innerHTML")
        for title in title_elements:
            role_title = title.get_attribute("innerHTML")
            break
        role_data.append(TitleLink(role_title, role_link))
        
    return role_data


def get_prompts_links(url,driver):
    driver.get(url)
    prompts_data = []
    prompt_title = ""
    prompt_link =""
    prompt_title_xpath = "//p[@class='prompt-txt']"
    prompt_xpath = "//a[contains(@class, 'prompt-item') and contains(@class, 'w-inline-block')]"

    prompt_selector =  wait.until(EC.presence_of_all_elements_located((By.XPATH,prompt_xpath)))
    for prompt in prompt_selector:    
        prompt_link = prompt.get_attribute("href")
        text_element = prompt.find_element(By.XPATH, "./p[@class='prompt-txt']")
        prompt_title = text_element.get_attribute("innerHTML")
        prompts_data.append(TitleLink(prompt_title,prompt_link))
    return prompts_data
    


def get_prompts_content(url,driver):
    driver.get(url)
    try:
        prompt_content_xpath = "//p[contains(@class, 'ms-comment')]"
        prompt_content_selector = wait.until(EC.presence_of_all_elements_located((By.XPATH,prompt_content_xpath)))
        for prompt_item in prompt_content_selector:
            prompts_text = prompt_item.get_attribute("innerHTML")
            if prompts_text.startswith('{'):
                print("prompt found")
                return prompt_item.get_attribute("innerHTML")
            else:
                
                print("No prompt found")
    except Exception:
        return ""



if __name__ == "__main__":
    options = Options()
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.1")
    url="https://www.aiforwork.co/"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    wait.until(EC.url_to_be(url))
    
    get_department_links(driver)