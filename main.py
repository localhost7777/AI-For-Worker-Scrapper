from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import csv

IS_DEBUG = False

def write_to_csv(fileName,data):
    csv_file_path = fileName
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["DepartmentLink", "RoleLink", "PromptLink","PromptText"])  # Write header row
        writer.writerows(data)
    print("Data has been written to", csv_file_path)

def get_department_links(driver):
    for_csv = []
    department_links = []
    department_xpath = "//a[contains(@class, 'bnnr-elmntbx-wrap') and contains(@class, 'elemntbx_main') and contains(@class, 'w-inline-block')]"
    department_selector =  wait.until(EC.presence_of_all_elements_located((By.XPATH,department_xpath)))
    
    for department in department_selector:
        department_links.append(department.get_attribute("href"))
        if IS_DEBUG:
            break
    
    for department in department_links:
        print(department)
        for role in get_roles_links(department,driver):
            print(role)
            for prompt_link in get_prompts_links(role,driver):
                print(prompt_link)
                prompt_content = get_prompts_content(prompt_link,driver)
                print(prompt_content)
                for_csv.append([department,role,prompt_link,prompt_content])
    write_to_csv("lol.csv",for_csv)

def get_roles_links(url,driver):
    driver.get(url)
    role_links = []
    wait.until(EC.url_to_be(url))
    role_xpath = "//a[contains(@class, 'bnnr-elmntbx-wrap') and contains(@class, 'elemntbx_main') and contains(@class, 'w-inline-block')]"
    role_selector =  wait.until(EC.presence_of_all_elements_located((By.XPATH,role_xpath)))
    for role in role_selector:
        role_links.append(role.get_attribute("href")) 
        if IS_DEBUG:
            break
    return role_links


def get_prompts_links(url,driver):
    driver.get(url)
    prompts_links = []
    prompt_xpath = "//a[contains(@class, 'prompt-item') and contains(@class, 'w-inline-block')]"
    prompt_selector =  wait.until(EC.presence_of_all_elements_located((By.XPATH,prompt_xpath)))
    for prompt in prompt_selector:
        prompts_links.append(prompt.get_attribute("href"))
        if IS_DEBUG:
            break
    print(prompts_links)
    return prompts_links
    


def get_prompts_content(url,driver):
    driver.get(url)
    prompts_text = []
    try:
        prompt_content_xpath = "//p[contains(@class, 'ms-comment')]"
        prompt_content_selector = wait.until(EC.presence_of_all_elements_located((By.XPATH,prompt_content_xpath)))
        for prompt in prompt_content_selector:
            prompt_text = prompt.get_attribute("innerHTML")
            if prompt_text.startswith('{'):
                return prompt_text
    except Exception:
        return ""



if __name__ == "__main__":
    options = Options()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    url="https://www.aiforwork.co/"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    wait.until(EC.url_to_be(url))
    print(driver.title)
    get_department_links(driver)