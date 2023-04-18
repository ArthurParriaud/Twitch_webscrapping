from selenium import webdriver
import time
import json
from selenium.webdriver.common.by import By
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

driver = webdriver.Chrome('chromedriver')
driver.get("https://www.twitch.tv/directory?sort=VIEWER_COUNT")

Game_data = dict()
Game_data['Category'] = []
Game_data['Viewer'] = []
Game_data['Tag'] = []
Game_data['Link'] = []
def Viewer2Int(Viewer):
    Viewer = Viewer.replace(",", ".")
    if "k" in Viewer:
        return float(Viewer.split(" k")[0])*1000
    else:
        return float(Viewer.split(" spec")[0])


def getTag(i):
    path_category1 = '//*[@id="browse-root-main-content"]/div[4]/div/div[1]/div[' + str(i) + ']/div/div/div/div/div[2]/div/div[1]/button/div/div/span'
    path_category2 = '//*[@id="browse-root-main-content"]/div[4]/div/div[1]/div[' + str(i) + ']/div/div/div/div/div[2]/div/div[2]/button/div/div/span'
    path_category3 = '//*[@id="browse-root-main-content"]/div[4]/div/div[1]/div[' + str(i) + ']/div/div/div/div/div[2]/div/div[3]/button/div/div/span'
    Tags = []
    try:
        Tags.append(driver.find_element(By.XPATH,path_category1).text)
        Tags.append(driver.find_element(By.XPATH, path_category2).text)
        Tags.append(driver.find_element(By.XPATH, path_category3).text)
    except:
        return Tags
    return Tags

def getCategory(n):
    for i in range(2,n + 2):
        path_name = '//*[@id="browse-root-main-content"]/div[4]/div/div[1]/div['+str(i)+']/div/div/div/div/div[1]/div/div/div/div/span/a/h2'
        path_viewer = '//*[@id="browse-root-main-content"]/div[4]/div/div[1]/div['+str(i)+']/div/div/div/div/div[1]/div/div/p/a'
        path_link = '//*[@id="browse-root-main-content"]/div[4]/div/div[1]/div['+str(i)+']/div/div/div/div/div[1]/div/div/div/div/span/a'

        Game_data['Category'].append(driver.find_element(By.XPATH,path_name).text)
        Game_data['Viewer'].append(Viewer2Int(driver.find_element(By.XPATH,path_viewer).text))
        Game_data['Tag'].append(getTag(i))
        Game_data['Link'].append(driver.find_element(By.XPATH,path_link).get_attribute('href'))
        time.sleep(1)

def createJSON(data):
    with open('sample.json','w') as outfile:
        json.dump(data, outfile, indent=4)

def dataviz(json_file):
    df = pd.read_json(json_file)
    plt.figure(figsize=(15, 20))
    sns.set(rc={'figure.figsize': (15, 20)})
    sns.barplot(x='Category', y='Viewer', data=df)
    plt.xticks(rotation=45, ha='right', fontsize=16)
    plt.yticks(fontsize=16)
    plt.title('Viewer by Category', fontsize=25)
    plt.xlabel('Category', fontsize=20)
    plt.ylabel('Viewer', fontsize=20)
    plt.show()

def main():
    getCategory(10)
    print(Game_data)
    createJSON(Game_data)
    dataviz('sample.json')
main()

