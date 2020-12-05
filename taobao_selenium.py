import time  # 进行延时
import random  # 产生随机数
from lxml import etree  # 解析网页
from selenium import webdriver  # 调用网页驱动


class Taobaoinfos:

    def __init__(self):
        url = 'https://www.taobao.com/'
        self.url = url
        self.browser = webdriver.Chrome(r'D:\Download\ChromeDriver.exe')

    def login(self):
        self.browser.get(self.url)
        self.browser.maximize_window()  # 最大化窗口
        # 扫码登录
        login_button = self.browser.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]')
        login_button.click()
        time.sleep(1.5)
        QRcode_button = self.browser.find_element_by_xpath('//*[@id="login"]/div[1]/i')
        QRcode_button.click()
        print('请扫码登录')
        while 1:
            jump_flag = self.browser.find_elements_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[2]/a')
            if jump_flag:
                print('扫码成功')
                break

    def search_goods(self, goodname):
        # 进行搜索
        search_input = self.browser.find_element_by_xpath('//div/input')
        search_input.send_keys(goodname)
        time.sleep(1)
        search_button = self.browser.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button')
        search_button.click()
        time.sleep(2)
        sort_button = self.browser.find_element_by_xpath('//*[@id="J_relative"]/div[1]/div/ul/li[2]/a')
        sort_button.click()

    def get_goodsinfos(self):
        # 获取页面信息
        page = self.browser.page_source
        page = etree.HTML(page)
        goods_local = page.xpath('//div[@class="items"]/div/div[2]/div[3]/div[2]/text()')  # 商品产地
        goods_price = page.xpath('//div[@class="items"]/div/div[2]/div[1]/div/strong/text()')  # 商品价格
        goods_sellnum = page.xpath('//div[@class="items"]/div/div[2]/div[1]/div[2]/text()')  # 商品销售数量
        for j in range(len(goods_local)):
            goods = goods_local[i] + ',' + goods_price[i] + ',' + goods_sellnum[i]
            f.write(goods + '\n')

    def rollpage(self):
        # 模拟滑动页面
        for j in range(4):
            self.browser.execute_script('window.scrollBy(0,1050)')
            time.sleep(random.random() * 1.2)

    def clicknextpage(self):
        # 点击下一页
        nextpage_button = self.browser.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[2]/span[3]')
        nextpage_button.click()


if __name__ == '__main__':
    name = input('请输入想要搜索的商品信息：')
    infos = Taobaoinfos()
    infos.login()
    infos.search_goods(name)
    with open('goodsinfo.csv', 'a', newline='', encoding='utf-8-sig') as f:
        try:
            for i in range(50):
                print(f'正在爬取第{i+1}页')
                infos.rollpage()
                infos.get_goodsinfos()
                infos.clicknextpage()
                time.sleep(random.random() * 6)
        except:
            print('爬取失败')
        else:
            print('爬取完成，完美！')
