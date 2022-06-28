import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from datetime import datetime, timedelta
import pandas as pd
import os

BASE_DIR = os.path.realpath('.')

posts_link=[]
class TwitterScript():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)


    def get_data(self,urls):
        data = []
        for u in urls:
            username=u.split('/')[-1]
            self.driver.get(u)
            sleep(6)
            name=self.driver.find_elements_by_xpath('//*[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]')[6].text
            join_date=self.driver.find_element_by_xpath('//*[@data-testid="UserJoinDate"]').text
            try:
                location=self.driver.find_element_by_xpath('//*[@data-testid="UserLocation"]').text
            except:
                location=''
            try:
                description=self.driver.find_element_by_xpath('//*[@data-testid="UserDescription"]').text
            except:
                description=''
            try:
                urls=self.driver.find_element_by_xpath('//*[@data-testid="UserUrl"]').get_attribute('href')
            except:
                urls=''
            followers=self.driver.find_element_by_xpath('//a[@href="/'+str(username)+'/followers"]').text
            following=self.driver.find_element_by_xpath('//a[@href="/'+str(username)+'/following"]').text
            followers=followers.replace(' followers','')
            following=following.replace(' following','')
            join_date=join_date.replace('Joined ','')
            data.append([name,location,description,join_date,urls,following,followers])

        dff=pd.DataFrame(data)
        dff.to_csv('results.csv',index=False)
obb = TwitterScript()

df=pd.read_csv('twitter_profiles.csv')
urls=df['Url'].tolist()

obb.get_data(urls)
