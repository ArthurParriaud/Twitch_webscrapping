import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TwitchDriver:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def viewer_count2Int(self, viewer_count):
        viewer_count = viewer_count.replace(',', '.')
        if 'k' in viewer_count:
            return int(float(viewer_count.split(" ")[0]) * 1000)
        else:
            return int(viewer_count.split(" ")[0])

    def get_categories(self, count=10):
        categories = [[], [], [], []]
        self.driver.get("https://www.twitch.tv/directory?sort=VIEWER_COUNT")
        time.sleep(2)

        path_category = '//*[@id="browse-root-main-content"]/div[4]/div/div[1]/div['
        path_name = './div/div/div/div/div[1]/div/div/div/div/span/a/h2'
        path_viewer_count = './div/div/div/div/div[1]/div/div/p/a'
        path_link = path_viewer_count

        for i in range(count):
            category_element = self.driver.find_element(By.XPATH, path_category + str(i+2) + ']')

            name = category_element.find_element(By.XPATH, path_name).text
            viewer_count = category_element.find_element(By.XPATH, path_viewer_count).text
            link = category_element.find_element(By.XPATH, path_link).get_attribute('href')
            tags = self.get_tags(category_element, './div/div/div/div/div[2]/div/div')

            categories[0].append(name)
            categories[1].append(self.viewer_count2Int(viewer_count))
            categories[2].append(tags)
            categories[3].append(link)
        return categories

    def get_tags(self, element, path):
        tags_list = []
        tags = element.find_elements(By.XPATH, path)
        for tag in tags:
            tags_list.append(tag.find_element(By.XPATH, './button/div/div/span').text)
        return tags_list

    def get_top_streams(self, category_url_list, count=10):
        top_streams = []
        for url in category_url_list:
            streams_infos = []
            self.driver.get(url + "?sort=VIEWER_COUNT")
            time.sleep(2)

            streams_div = self.driver.find_element(By.XPATH, '//*[@id="directory-game-main-content"]/div[4]/div/div[2]/div[1]')
            for i in range(count):
                stream_element = streams_div.find_element(By.XPATH, './div[' + str(i+2) + ']')
                viewer_count = stream_element.find_element(By.XPATH, './div/div/div/article/div[2]/div[5]/a/div/div[3]/div').text
                name = stream_element.find_element(By.XPATH, './div/div/div/article/div[1]/div/div[1]/div[1]/a/p').text
                tags = self.get_tags(stream_element, './div/div/div/article/div[1]/div/div[1]/div[2]/div/div')
                streams_infos.append([name, self.viewer_count2Int(viewer_count), tags])

            top_streams.append(streams_infos)
        return top_streams