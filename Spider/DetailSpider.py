import csv
import csv
import time
import re
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree

class LagouJobDetail(object):
    driver_path = r'D:\chromedriver\chromedriver.exe'

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.job_urls = []
        self.login_url = 'https://passport.lagou.com/login/login.html'
        self.test_job_urls = []
        self.job_detail = []
        self.headers = ['职位名称', '薪资', '工作城市', '工作地点', '工作经验', '职位链接',
                        '教育程度', '工作状况', '职位标签', '发布时间', '公司名称',
                        '公司标签', '融资情况', '公司人数', '职位诱惑', '职位描述']
        self.error_url = []

    def run(self):
        self.driver.get(self.login_url)
        self.login()
        time.sleep(20)
        with open('job_url.csv', 'r', encoding='GBK') as fp:
            reader = csv.DictReader(fp)
            for x in reader:
                self.job_urls.append(x['job_url'])
        with open('detail.csv', 'r', encoding='UTF-8') as fp:
            reader = csv.DictReader(fp)
            for x in reader:
                self.test_job_urls.append(x['职位链接'])
        try:
            for job_url in self.job_urls:
                if job_url not in self.test_job_urls:
                    time.sleep(4.4)
                    self.driver.get(job_url)
                    page = self.driver.page_source
                    self.parse(page, job_url)
            with open('detail.csv', 'a', newline='', encoding='UTF-8') as fp:
                writer = csv.DictWriter(fp, self.headers)
                # writer.writeheader()
                writer.writerows(self.job_detail)
        except Exception as e:
            print(e)
            with open('detail.csv', 'a', newline='', encoding='UTF-8') as fp:
                writer = csv.DictWriter(fp, self.headers)
                # writer.writeheader()
                writer.writerows(self.job_detail)

    def parse(self, page, job_url):
        try:
            html = etree.HTML(page)
            position_name = html.xpath("//div[@class='job-name']//h2[@class='name']/text()")[0]
            salary = html.xpath("//dd[@class='job_request']//span[1]/text()")[0]
            position_place = html.xpath("//dd[@class='job_request']//span[2]/text()")[0].replace('/', '')
            position_place_details = html.xpath("//div[@class='work_addr']//text()")[:-1]
            position_place_detail = "".join(list(map(lambda x: x.strip(), position_place_details)))
            work_years = html.xpath("//dd[@class='job_request']//span[3]/text()")[0].replace('/', '')
            education = html.xpath("//dd[@class='job_request']//span[4]/text()")[0].replace('/', '')
            work_condition = html.xpath("//dd[@class='job_request']//span[5]/text()")[0]
            position_label = ",".join(html.xpath("//ul[@class='position-label clearfix']/li/text()"))
            publish_time = html.xpath("//p[@class='publish_time']/text()")[0].split('发')[0].strip()
            company = html.xpath("//div[@class='job_company_content']//em[@class='fl-cn']/text()")[0].strip()
            company_label = html.xpath("//ul[@class='c_feature']/li[1]/h4[@class='c_feature_name']/text()")[0]
            company_condition = html.xpath("//ul[@class='c_feature']/li[2]/h4[@class='c_feature_name']/text()")[0]
            company_people = html.xpath("//ul[@class='c_feature']/li[3]/h4[@class='c_feature_name']/text()")[0]
            job_advantage = "".join(html.xpath("//dd[@class='job-advantage']/p/text()"))
            job_description = "".join(html.xpath("//div[@class='job-detail']//text()")).strip()
            position = {
                '职位名称': position_name,
                '薪资': salary,
                '工作城市': position_place,
                '工作地点': position_place_detail,
                '工作经验': work_years,
                '教育程度': education,
                '工作状况': work_condition,
                '职位标签': position_label,
                '发布时间': publish_time,
                '公司名称': company,
                '公司标签': company_label,
                '融资情况': company_condition,
                '公司人数': company_people,
                '职位诱惑': job_advantage,
                '职位描述': job_description,
                '职位链接': job_url
            }
            self.job_detail.append(position)
        except Exception as e:
            print(e)
            print(job_url + '解析错误')
            self.error_url.append(job_url)

    def login(self):
        account = self.driver.find_element_by_xpath("//div[@data-propertyname='username']/input")
        pwd = self.driver.find_element_by_xpath("//div[@data-propertyname='password']/input")
        submit = self.driver.find_element_by_xpath("//input[@type='submit']")
        action = ActionChains(self.driver)
        action.send_keys_to_element(account, '15217811087')
        action.send_keys_to_element(pwd, '145632789')
        action.click(submit)
        action.perform()


if __name__ == '__main__':
    LagouJobDetail().run()
