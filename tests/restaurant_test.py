from magarimame.restaurant import Restaurant


class TestRestaurant:
    def test_select_all(self):
        restaurant = Restaurant()
        for data in restaurant.select_all():
            name = data[1]
            address = data[3]
            link = data[4]
            print(
                """name    : {}
address : {}
link    : {}
-----------------------------""".format(
                    name, address, link
                )
            )
