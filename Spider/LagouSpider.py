import csv
import time
import re
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class LagouJobUrl(object):
    driver_path = r'D:\chromedriver\chromedriver.exe'

    def __init__(self):
        self.url = []
        self.headers = ['city_name', 'job_url']
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.login_url = 'https://passport.lagou.com/login/login.html'
        self.all_citys_url = 'https://www.lagou.com/jobs/allCity.html?keyword=python&px=default'
        self.large_city = ['北京', '上海', '深圳', '广州', '杭州', '成都', '武汉']

    def close_window(self, page):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[page])

    def open_window(self, url, page):
        self.driver.execute_script("window.open('%s')" % url)
        self.driver.switch_to.window(self.driver.window_handles[page])

    def get_totalpage(self):
        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='page-number']/span[last()]"))
        )
        totalpage = self.driver.find_element_by_xpath("//div[@class='page-number']/span[last()]").text
        totalpage = int(totalpage)
        return totalpage

    # 获取0个数据
    def get_none_city(self, city_name, district_name=None,bizareas_name=None):
        city = {
             'job_url': '该城市没有相关职位',
            'city_name': city_name
        }
        if district_name:
            city['city_name'] = city_name+district_name
        if bizareas_name:
            city['city_name'] = city_name + district_name + bizareas_name
        self.url.append(city)
        if bizareas_name:
            self.close_window(1)
        # else:
        #     self.close_window(0)

    # 获取一页数据
    def get_one_page_city(self, city_name, district_name=None,bizareas_name=None):
        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='position']//a[@class='position_link']"))
        )
        job_detail_urls = self.driver.find_elements_by_xpath(
            "//div[@class='position']//a[@class='position_link']")
        for job_detail_url in job_detail_urls:
            job_detail_url = job_detail_url.get_attribute('href')
            city = {
                'job_url': job_detail_url,
                'city_name': city_name
            }
            if district_name:
                city['city_name'] = city_name + district_name
            if bizareas_name:
                city['city_name'] = city_name + district_name + bizareas_name
            self.url.append(city)
        if bizareas_name:
            self.close_window(1)
        # 爬取小城市的时候取消注释
        # else:
        #     self.close_window(0)

    # 获取当前页面的所有职位链接，对城市名进行处理，当当前页数等于最大页数的时候，退出循环
    # 发生找不到页面元素异常的时候重新执行
    def get_many_page_city(self, city_name, district_name=None, bizareas_name=None):
        try:
            while True:
                WebDriverWait(driver=self.driver, timeout=10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='position']//a[@class='position_link']"))
                )
                totalpage = self.get_totalpage()
                job_detail_urls = self.driver.find_elements_by_xpath(
                    "//div[@class='position']//a[@class='position_link']")
                for job_detail_url in job_detail_urls:
                    job_detail_url = job_detail_url.get_attribute('href')
                    city = {
                        'job_url': job_detail_url,
                        'city_name': city_name
                    }
                    if district_name:
                        city['city_name'] = city_name + district_name
                    if bizareas_name:
                        city['city_name'] = city_name + district_name + bizareas_name
                    self.url.append(city)
                WebDriverWait(driver=self.driver, timeout=10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='pager_container']/span[@class='pager_is_current']"))
                )
                current_page = self.driver.find_element_by_xpath(
                    "//div[@class='pager_container']/span[@class='pager_is_current']")
                current_page = int(current_page.text)
                if current_page == totalpage:
                    if bizareas_name :
                        self.close_window(1)
                    # 爬取小城市的时候取消注释
                    # if not bizareas_name:
                    #     self.close_window(0)
                    break
                self.get_next()
        except StaleElementReferenceException as e:
            time.sleep(5)
            print(e)
            print('准备翻页出错啦')
            return self.get_many_page_city(city_name, district_name=district_name, bizareas_name=bizareas_name)

    # 获取下一页并点击
    def get_next(self):
        try:
            WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='pager_container']/span[last()]"))
            )
            next_bt = self.driver.find_element_by_xpath("//div[@class='pager_container']/span[last()]")
            time.sleep(6)
            next_bt.click()
        except Exception as e:
            print('翻页出错了')

    # 按照城市列表遍历打开城市，如何处理城市信息交给get_large_city_url和get_small_city_url
    def open_get_city_urls(self):
        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='city_list']//input"))
        )
        inputs = self.driver.find_elements_by_xpath("//ul[@class='city_list']//input")
        for input in inputs:
            city_url = input.get_attribute('value')
            city_url = re.sub('#filterBox', '', city_url).strip()
            city_name = city_url.split('city=')[1]
            self.get_large_city_url(city_name, city_url)
            self.get_small_city_url(city_name, city_url)

    # 获取大城市的职位链接，这样的城市特点是城市有30页，区可能也有30页、0页、1页、多页，
    # 区里面的范围可能也有30页、0页、1页、多页
    def get_large_city_url(self, city_name, city_url):
        if city_name in self.large_city:
            self.open_window(city_url, 1)
            district_names = self.driver.find_elements_by_xpath("//div[@data-type='district']/a")
            district_names = list(map(lambda district_name: district_name.text, district_names))[0]
            district_urls = list(map(lambda district_name: self.driver.current_url.split('#')[0] + '&district=' + district_name, district_names))
            for district_url in district_urls:
                time.sleep(3)
                self.driver.get(district_url)
                district_name = district_url.split('district=')[1]
                totalpage = self.get_totalpage()
                if totalpage == 0:
                    self.get_none_city(city_name, district_name)
                elif totalpage == 1:
                    self.get_one_page_city(city_name, district_name)
                elif totalpage < 30 and totalpage != 0:
                    self.get_many_page_city(city_name, district_name)
                elif totalpage == 30:
                    self.get_bizarea_url(city_name, district_name)

    # 获取范围链接，范围链接为区域链接加范围名，不限的范围名过滤
    # 区域的链接可能没有数据，可能只有一条，可能有多条需要翻页
    def get_bizarea_url(self, city_name, district_name):
        bizareas_names = self.driver.find_elements_by_xpath("//div[@class='detail-items']/a")
        bizareas_names = list(map(lambda bizareas_name: bizareas_name.text, bizareas_names))[1:]
        bizarea_urls = list(map(lambda big_area_name: self.driver.current_url.split('#')[0] + '&bizArea=' + big_area_name, bizareas_names))
        for bizarea_url in bizarea_urls:
            time.sleep(3)
            self.open_window(bizarea_url, 2)
            bizareas_name = bizarea_url.split('&bizArea=')[1]
            totalpage = self.get_totalpage()
            if totalpage == 0:
                self.get_none_city(city_name, district_name, bizareas_name)
            elif totalpage == 1:
                self.get_one_page_city(city_name, district_name, bizareas_name)
            else:
                self.get_many_page_city(city_name, district_name=district_name, bizareas_name=bizareas_name)

# 获取小城市的职位链接，特点是这个城市的职位不超过30页
#     当前页数为一页的时候是没有下一页按钮的
    def get_small_city_url(self, city_name, city_url):
        if city_name not in self.large_city:
            self.open_window(city_url, 1)
            totalpage = self.get_totalpage()
            if totalpage == 0:
                time.sleep(4)
                self.get_none_city(city_name)
            elif totalpage == 1:
                time.sleep(4)
                self.get_one_page_city(city_name)
            else:
                self.get_many_page_city(city_name, totalpage)

# 登录后进到全国城市链接，打开并遍历每一个城市，完成遍历后写入csv，发生异常将异常前的数据写入
    def run(self):
        try:
            self.driver.get(self.login_url)
            self.login()
            time.sleep(20)
            self.driver.get(self.all_citys_url)
            self.open_get_city_urls()
            with open('test.csv', 'a', newline='', encoding='UTF-8') as fp:
                writer = csv.DictWriter(fp, self.headers)
                writer.writeheader()
                writer.writerows(self.url)
        except:
            with open('test.csv', 'a', newline='', encoding='UTF-8') as fp:
                writer = csv.DictWriter(fp, self.headers)
                # writer.writeheader()
                writer.writerows(self.url)

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
    LagouJobUrl().run()
