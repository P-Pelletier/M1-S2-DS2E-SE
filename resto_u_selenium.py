from selenium import webdriver
from selenium.webdriver.firefox.options import Options  
from selenium.webdriver.common.by import By

firefox_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
firefox_options.set_preference("general.useragent.override", user_agent)

driver = webdriver.Firefox(
    options=firefox_options
)

driver.get("https://www.crous-strasbourg.fr/restaurant/resto-u-esplanade/")

menu_elements = driver.find_elements(By.CLASS_NAME, "menu")

menu_element = menu_elements[0]
time_element = menu_element.find_element(By.CLASS_NAME, "menu_date_title")
date = time_element.text.replace('Menu du ', '')
print(date)

meal_elements = menu_element.find_elements(By.CLASS_NAME, "meal")
meal_element = meal_elements[0]   
print(meal_element)

meal_type = meal_element.find_element(By.CLASS_NAME, "meal_title").text

meal_infos = meal_element.find_element(By.CLASS_NAME, "meal_foodies").get_attribute("innerHTML")
meal_by_poles = re.findall("<li>(.*?)</li></ul></li>",meal_infos)

meal_by_pole = meal_by_poles[0]

pole, meal_infos = meal_by_pole.split("<ul><li>")
meal_infos = meal_infos.split('</li><li>')
meal_infos = [meal for meal in meal_infos if meal != '-']


def get_all_links():
    urlpage = 'https://www.crous-strasbourg.fr/se-restaurer/ou-manger/'
    driver.get(urlpage)
    elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/restaurant/')]")
    
    names_links = dict()
    for element in elements:
        link = element.get_attribute("href")
        if '/restaurant/' in link:
            link = str(link)
            name = re.findall('restaurant/(.*)/',link)[0]
            name = re.sub('-',' ',name)
            name = re.sub(' 2','',name)
            name = name.title()
            names_links.update({name:link})

    return names_links
