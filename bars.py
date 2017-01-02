import json
import codecs
import os.path
import sys
import math


def load_data(filepath):
    if os.path.exists(filepath):
        with codecs.open(filepath, "r", "cp1251") as data_file:
            return json.loads(data_file.read())
    else:
        return None


def get_biggest_bar(data):
    biggest_bar = max(data, key=lambda x: x["SeatsCount"])
    return biggest_bar["Name"], biggest_bar["SeatsCount"]


def get_smallest_bar(data):
    smallest_bar = min(data, key=lambda x: x["SeatsCount"])
    return smallest_bar["Name"], smallest_bar["SeatsCount"]


def circ_dist(long1, lat1, long2, lat2):
    long1, lat1, long2, lat2 = map(math.radians, [long1, lat1, long2, lat2])
    sin1 = math.sin(lat1)
    sin2 = math.sin(lat2)
    cos1 = math.cos(lat1)
    cos2 = math.cos(lat2)
    cos12 = math.cos(long2 - long1)
    return 6367444.6571225 * math.acos(sin1 * sin2 + cos1 * cos2 * cos12)


def get_closest_bar(data, longitude, latitude):
    long = float(longitude)
    lat = float(latitude)
    closest_bar = min(data, key=lambda x: circ_dist(long, lat,
                                                    x["geoData"]["coordinates"][1],
                                                    x["geoData"]["coordinates"][0]))
    min_dist = round(
        circ_dist(long, lat,
                  closest_bar["geoData"]["coordinates"][1],
                  closest_bar["geoData"]["coordinates"][0]) / 1000, 2)
    return closest_bar["Name"], min_dist


if __name__ == '__main__':
    bars_data = load_data(sys.argv[1])
    if bars_data:
        biggest_bar = get_biggest_bar(bars_data)
        smallest_bar = get_smallest_bar(bars_data)
        print("Самый большой бар: ", biggest_bar[0], ". Число мест: ", biggest_bar[1])
        print("Самый маленький бар: ", smallest_bar[0], ". Число мест: ", smallest_bar[1])
        print("Для поиска ближайшего бара необходимо ввести ваши координаты")
        latitude = input("Введите широту: ")
        longitude = input("Введите долготу: ")
        closest_bar = get_closest_bar(bars_data, longitude, latitude)
        print("Ближайший бар: ", closest_bar[0], ". Расстояние до него: ", closest_bar[1], " км.")
    else:
        print("Не удалось прочитать файл")
