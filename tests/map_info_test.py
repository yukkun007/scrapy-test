from magarimame.map_info import MapInfo


class TestMapInfo:
    def test_is_already_exist_false(self):
        map_info = MapInfo()
        assert map_info.is_already_exist("test") is False

    def test_is_already_exist_true(self):
        map_info = MapInfo()
        assert map_info.is_already_exist("船場吉兆") is True

    def test_save(self):
        map_info = MapInfo()
        item = {
            "name": "hoge",
            "lat": "35.11111",
            "lon": "130.11111",
            "link": "https://www.google.co.jp",
        }
        map_info.save(item)

    def test_select_all(self):
        map_info = MapInfo()
        for data in map_info.select_all():
            name = data[1]
            lat = data[2]
            lon = data[3]
            link = data[4]
            print(
                """name : {}
lat  : {}
lon  : {}
link : {}
-----------------------------""".format(
                    name, lat, lon, link
                )
            )
