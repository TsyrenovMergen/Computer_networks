import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


rep_dir=os.listdir('Котомышь_реплеи')
path_files=[]

for file in rep_dir:
    path_files.append(os.path.abspath("Котомышь_реплеи\\"+file))

browser = webdriver.Chrome()
browser.get('https://wc3stats.com/')
browser.find_element(By.CSS_SELECTOR, "body > div > div.container.container--ultrawide > nav >"\ 
                                      "div.W3S-navbar__links > div.W3S-navbar__links--left > a:nth-child(4)").click()
upload_files_element=browser.find_element(By.CSS_SELECTOR, "#replay")

for path in path_files:
    upload_files_element.send_keys(path)

browser.find_element(By.CSS_SELECTOR, "body > div > div.container.container--ultrawide > nav >"\
                                      "div.W3S-navbar__links > div.W3S-navbar__links--left > a:nth-child(2) > span").click()
links=[]
names=[]

while(1):
    flag=1
    time.sleep(3)
    new_elements=browser.find_elements(By.CLASS_NAME, "Row.clickable.Row-body")
    for element in new_elements:
        if "КОТОМЫШЬ" in element.text.strip():
            flag=0
            names.append(element.text.strip())
            links.append(element.get_attribute('href'))
    browser.find_element(By.CSS_SELECTOR, "body > div > main > div > div.Splash-content > div > div > div > div.Table-controls.top > div.paging > ul > li:nth-child(11) > a > i").click()
    if flag==1:
        break

browser.quit()
colors_name=['red', 'blue', 'teal', 'purple', 'yellow', 'orange', 'green', 'pink', 'grey', 'light-blue', 'dark-green', 'brown']


def info_one_game(link, name_game, index):
    name_game=name_game.split()
    name_game=name_game[0]+" "+name_game[1]
    browser_game = webdriver.Chrome()
    browser_game.get(link)
    time.sleep(1)
    elements=browser_game.find_elements(By.CLASS_NAME, "col-6")
    time_game=elements[3].text.strip()
    data=elements[9].text.strip()
    browser_game.find_element(By.CSS_SELECTOR, "body > div > main > div > div.PageGutter > div.Tabs > a:nth-child(3)").click()
    names=[]
    statuses=[]
    colors=[]
    time.sleep(1)
    gamers=browser_game.find_elements(By.TAG_NAME, "tr")
    for gamer in gamers:
        text=gamer.text.strip()
        text=text.split()
        names.append(text[0])
        if len(text)==2:
            statuses.append(text[1])
        else:
            statuses.append("N/A")
    time.sleep(1)
    iconks=browser_game.find_elements(By.TAG_NAME, "td")
    for iconk in iconks:
        color=iconk.get_attribute("style")
        for number in range(12):
            if colors_name[number] in color and (number!=6 or not (colors_name[11] in color)):
                colors.append(number+1)
                break
    browser_game.quit() 
    with open('games\game_info'+str(index)+'.csv', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Название", "Время", "Дата"])
        writer.writerow([name_game, time_game, data])
        for i in range(len(names)):
            writer.writerow([colors[i], names[i], statuses[i]])


for i in range(len(links)):
    info_one_game(links[i], names[i], i)
