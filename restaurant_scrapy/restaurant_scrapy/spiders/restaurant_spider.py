import scrapy
import re
from restaurant_scrapy.items import Restaurant


class RestaurantSpider(scrapy.Spider):
    name = "restaurant_spider"
    allowed_domains = ["kakaku.com"]
    start_urls = ["https://kakaku.com/tv/channel=4/programID=23065/category=restaurant/"]
    page_num = 122

    def parse(self, response):
        for post in response.css(".box-bk .pdBtm20"):

            # 店名
            name = post.css(".tvnamebk p::text").extract_first().strip()
            # リンク
            link = ""
            link_element = post.css("a.tvnamebk::attr(href)").extract_first()
            if link_element is not None:
                link = link_element.strip()
            else:
                print(">>>>>>>>>>>>>>>>>")
                print("link is not found: at {}".format(name))
                print(">>>>>>>>>>>>>>>>>")
            # 住所
            area_info = post.css("ul.itemAddress li::text").extract_first().strip()
            address = area_info[area_info.rfind("住所：") + 3 :]
            # コメント
            info = ""
            info_element = post.css("div.iteminfo p::text").extract_first()
            if info_element is not None:
                info = info_element.strip()
            else:
                print(">>>>>>>>>>>>>>>>>")
                print("info is not found: at {}".format(name))
                print(">>>>>>>>>>>>>>>>>")

            p = re.compile("[0-9]+")
            if not (p.search(address)):
                # 数値が含まれない場合は、住所検索に店名を使う
                address = name
                print(">>>>>>>>>>>>>>>>>")
                print("address is about: at {}".format(name))
                print(">>>>>>>>>>>>>>>>>")

            print(".............................")
            print(address)
            print(".............................")

            yield Restaurant(
                name=name, info=info, address=address, link=link,
            )

        now = response.css(".navibox ul.count li.now::text").extract_first().strip()
        print(".............................")
        print("current page num={}".format(now))
        print(".............................")
        if now == "1":
            return

        # https://kakaku.com/tv/channel=4/programID=23065/category=restaurant/page=122/
        RestaurantSpider.page_num = RestaurantSpider.page_num - 1
        older_post_link = (
            RestaurantSpider.start_urls[0] + "/page=" + str(RestaurantSpider.page_num) + "/"
        )
        yield scrapy.Request(older_post_link, callback=self.parse)
