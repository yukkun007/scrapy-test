import time
import logging
import requests
import folium
import pandas as pd
from typing import List, Dict
from tqdm import tqdm
from bs4 import BeautifulSoup
from magarimame.restaurant import Restaurant
from magarimame.map_info import MapInfo


def _get_latlon_from_address(restaurants_data: List[Dict]) -> List[Dict]:
    # https://www.geocoding.jp/api/
    url = "http://www.geocoding.jp/api/"
    new_restaurants_data = []
    for restaurant_data in tqdm(restaurants_data):
        name = restaurant_data["name"]
        address = restaurant_data["address"]
        link = restaurant_data["link"]

        payload = {"v": 1.1, "q": address}
        response = requests.get(url, params=payload)
        # lxmlのインストールが必要
        # https://yukun.info/install-lxml/
        # easy_install lxml
        soup = BeautifulSoup(response.content, "lxml")
        if soup.find("error"):
            logging.error(f"invalid address submitted. {address}")
            # raise ValueError(f"invalid address submitted. {address}")
        else:
            lat = soup.find("lat").string
            lon = soup.find("lng").string
            new_restaurants_data.append({"name": name, "lat": lat, "lon": lon, "link": link})
            time.sleep(10)
    return new_restaurants_data


def _get_restaurants_data() -> List[Dict]:
    restaurant = Restaurant()
    map_info = MapInfo()
    data_list = []

    for data in restaurant.select_all():
        name = data[1]
        address = data[3]
        link = data[4]

        if map_info.is_already_exist(name):
            logging.info("skip get data. already exists. name={}".format(name))
        else:
            data_list.append({"name": name, "address": address, "link": link})

    return data_list


def _save_map_info(restaurants_data: List[Dict]):
    map_info = MapInfo()

    # address -----> lat, lon
    new_restaurants_data = _get_latlon_from_address(restaurants_data)
    for restaurant_data in new_restaurants_data:
        name = restaurant_data["name"]
        link = restaurant_data["link"]
        lat = restaurant_data["lat"]
        lon = restaurant_data["lon"]
        logging.info("save map info. name={}, lat={}, lon={}".format(name, lat, lon))
        item = {"name": name, "lat": lat, "lon": lon, "link": link}
        map_info.save(item)


def save_map_by_name_query(name: str):
    save_map(name, "by_name")


def save_map_by_info_query(info: str):
    save_map(info, "by_info")


def save_map(query: str = "", type: str = "all"):
    restaurant_list = []
    latitude_list = []
    longtude_list = []

    restaurant: Restaurant = Restaurant()

    data_list = None
    if type == "by_name":
        data_list = restaurant.select_by_name(query)
    elif type == "by_info":
        data_list = restaurant.select_by_info(query)
    else:
        data_list = restaurant.select_all()

    for data in data_list:
        name = data[1]

        map_info: MapInfo = MapInfo()
        # 常に1個のはず
        for map_data in map_info.select_by_name(name):
            name_of_map = map_data[1]
            lat = map_data[2]
            lon = map_data[3]
            link = map_data[4]

            restaurant_list.append("<a href='{}'>{}</a>".format(link, name_of_map))
            latitude_list.append(float(lat))
            longtude_list.append(float(lon))

    restaurants = pd.DataFrame(
        {"restaurant": restaurant_list, "latitude": latitude_list, "longtude": longtude_list}
    )

    map = folium.Map(location=[35.736489, 139.746875], zoom_start=5)
    for i, r in restaurants.iterrows():
        folium.Marker(location=[r["latitude"], r["longtude"]], popup=r["restaurant"]).add_to(map)

    map.save("map_shop.html")


def all():
    # dbからレストラン情報取得
    restaurants_data = _get_latlon_from_address()
    # gecode検索しながら、レストラン情報を別dbに保存
    _save_map_info(restaurants_data)
    # 地図生成
    save_map()


def main():
    # 地図生成
    # save_map_by_info_query("ステーキ")
    save_map()


if __name__ == "__main__":
    main()
