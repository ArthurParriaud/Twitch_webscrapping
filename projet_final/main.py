import datetime
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import twitchdriver
import json


def main():
    driver = twitchdriver.TwitchDriver()
    data = driver.get_categories(5)

    Category_data = dict()
    Category_data['Category'] = data[0]
    Category_data['Viewer'] = data[1]
    Category_data['Tag'] = data[2]
    Category_data['Link'] = data[3]
    langues = getViewerPerLanguage(driver, Category_data)
    Language_data = dict()
    Language_data['Language'] = []
    Language_data['NumberOfViewer'] = []
    for i in langues:
        Language_data['Language'].append(i[0])
        Language_data['NumberOfViewer'].append(i[1])

    createJSON(Language_data,'sample2')
    createJSON(Category_data,'sample')

    dataviz("sample.json")
    plot_langues_vues("sample2.json")

def createJSON(data,nom):
    with open(nom + '.json','w') as outfile:
        json.dump(data, outfile, indent = 4)

def getViewerPerLanguage(driver, data):
    data_top_streams = driver.get_top_streams(data['Link'], 10)
    langues = [["Français", 0], ["English", 0], ["Deutsch", 0], ["Español", 0], ["Italiano", 0], ["中文", 0], ["日本語", 0], ["العربية", 0]]
    for cat in data_top_streams:
        for stream in cat:
            for i in range(len(langues)):
                if(langues[i][0] in stream[2]):
                    langues[i][1] += stream[1]
    return langues


def dataviz(json_file):
    df = pd.read_json(json_file)
    plt.figure(figsize=(15, 20))
    sns.set(rc={'figure.figsize': (15, 20)})
    sns.barplot(x='Category', y='Viewer', data=df)
    plt.xticks(rotation=45, ha='right', fontsize=36)
    plt.yticks(fontsize=36)

    now = datetime.datetime.now()
    formatted_now = now.strftime("le %d/%m/%y à %Hh%Mmin%Ss")
    plt.title('Viewer by Category ' + formatted_now, fontsize=45)
    plt.xlabel('Category', fontsize=40)
    plt.ylabel('Viewer', fontsize=40)
    sns.despine()  # Remove the top and right spines
    plt.show()

def plot_langues_vues(json_file):
    df = pd.read_json(json_file)
    plt.figure(figsize=(15, 20))
    sns.set(rc={'figure.figsize': (15, 20)})
    sns.barplot(x='Language', y='NumberOfViewer', data=df)
    plt.xticks(rotation=45, ha='right', fontsize=36)
    plt.yticks(fontsize=36)

    now = datetime.datetime.now()
    formatted_now = now.strftime("le %d/%m/%y à %Hh%Mmin%Ss")
    plt.title('Viewer by Language ' + formatted_now, fontsize=45)
    plt.xlabel('Language', fontsize=40)
    plt.ylabel('NumberOfViewer', fontsize=40)
    sns.despine()  # Remove the top and right spines
    plt.show()


main()