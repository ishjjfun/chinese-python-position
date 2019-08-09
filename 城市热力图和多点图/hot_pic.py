import json
import time

import requests
import csv

class POINT_PIC():
    def __init__(self):
        self.str_temps = []
        self.job_places = []

    def get_baidu_api(self, address):
        url = 'http://api.map.baidu.com/geocoding/v3/'
        output = 'json'
        ak = 'xdL16a4vxShcgh2T50u8VvssXAZLlE35'
        uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
        res = requests.get(uri)
        res = json.loads(res.text)
        return res

    def get_point(self):
        with open('new_detail.csv', 'r', encoding='UTF-8') as fp:
            reader = csv.DictReader(fp)
            for x in reader:
                self.job_places.append(x['工作地点'])
        try:
            for job_place in self.job_places:
                res = self.get_baidu_api(job_place)
                res = json.loads(res.text)
                if res['status'] == 0:
                    lng = res['result']['location']['lng']
                    lat = res['result']['location']['lat']
                    str_temp = '{"lat":' + str(lat) + ',"lng":' + str(lng) + '},'
                    self.str_temps.append(str_temp + '\n')
                else:
                    continue
            with open('point.json', 'a', newline='') as fp1:
                fp1.writelines(self.str_temps)
        except Exception as e:
            print(e)
            with open('point.json', 'a', newline='') as fp1:
                fp1.writelines(self.str_temps)

    def get_city_hot(self):
        file = open(r'hot_point.json', 'w')  # 建立json数据文件
        with open(r'city_count.csv', 'r') as csvfile:  # 打开csv
            reader = csv.reader(csvfile)
            for line in reader:  # 读取csv里的数据
                city = line[0].strip()  # 将第一列city读取出来并清除不需要字符
                count = line[1].strip()  # 将第二列price读取出来并清除不需要字符
                lng = self.get_baidu_api(city)['result']['location']['lng']  # 采用构造的函数来获取经度
                lat = self.get_baidu_api(city)['result']['location']['lat']  # 获取纬度
                str_temp = '{"lat":' + str(lat) + ',"lng":' + str(lng) + ',"count":' + str(count) + '},'
                # print(str_temp) #也可以通过打印出来，把数据copy到百度热力地图api的相应位置上
                file.write(str_temp)  # 写入文档
        file.close()  # 保存

if __name__ == '__main__':
    point_pic = POINT_PIC()
    point_pic.get_city_hot()
