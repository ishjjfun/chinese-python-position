# chinese-python-position
全国Python职位的数据挖掘与分析，数据源来自拉勾600+个城市和地区
# Spider文件夹中是爬虫程序
拉勾的反爬虫很厉害，我采用的是selemiun+chormdriver先爬取职位链接
得到职位链接后再统一的爬取职位信息，以此来减少同一时间对拉勾服务器的请求量，
爬取链接的时候还分没有小区域的小城市和有区还有街道的大城市爬取，以最大的爬取数量来做数据分析
# 热力图文件夹
内部是两个HTML文件以及坐标转换的代码
# ipynb文件
这个是我的数据分析文件，更多解释可以点开文件头部观看
(电脑内没有anaconda可以用这个路径打开
https://nbviewer.jupyter.org/github/ishjjfun/chinese-python-position/blob/master/Python_job.ipynb)
# 其他文件
都是数据分析时生成的结果图片
job_url是所有链接的文件
detail是所有详情的文件
