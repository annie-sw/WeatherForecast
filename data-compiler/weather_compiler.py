# coding: utf-8
import csv
import json


MAP_SHEET = 'exd/Map.csv'
TERRITORY_TYPE_SHEET = 'exd/TerritoryType.csv'
WEATHER_SHEET = 'exd/Weather.csv'
WEATHER_RATE_SHEET = 'exd/WeatherRate.csv'
WEATHER_GROUP_SHEET = 'exd/WeatherGroup.csv'


def load_sheet(sheet_path):
    with open(sheet_path, 'r') as f:
        return [x for x in csv.reader(f)][3:]


def load_dict_sheet(sheet_path, col_idx, conv=lambda x: x):
    return {conv(x[col_idx]):x for x in load_sheet(sheet_path)}


def get_idx(map, id):
    #  if id in map:
        #  return map[id]

    #  idx = len(map)
    #  map[id] = idx
    #  return idx
    try:
        return map.index(id)
    except ValueError:
        idx = len(map)
        map.append(id)
        return idx


def main():
    map_sheet = load_sheet(MAP_SHEET)
    territory_type_sheet = load_dict_sheet(TERRITORY_TYPE_SHEET, 0, int)
    weather_rate_sheet = load_dict_sheet(WEATHER_RATE_SHEET, 0, int)
    weather_group_sheet = load_dict_sheet(WEATHER_GROUP_SHEET, 0, int)

    weather_group_map = {
        128: 0,
        129: 1,
        130: 2,
        131: 14,
        132: 15,
        133: 7,
        134: 8,
        135: 32,
        136: 34,
        137: 33,
        138: 48,
        139: 47,
        140: 0,
        141: 82,
    }

    place_name_map = []
    weather_name_map = []
    weather_rate_map = []

    place_list = []
    weather_rate_list = []

    for row in map_sheet:
        id_str = row[5 + 1].strip()
        if not id_str:
            continue

        region = int(row[9 + 1])
        name = int(row[10 + 1])

        territory_id = int(row[14 + 1])
        territory = territory_type_sheet.get(territory_id)
        if not territory:
            continue

        weather_rate_id = int(territory[12 + 1])
        if weather_rate_id < 0:
            continue

        # TODO: weather group
        #  weather_rate_id = weather_group_sheet.get(weather_rate_id, weather_rate_id)
        weather_rate_id = weather_group_map.get(weather_rate_id, weather_rate_id)

        weather_rate = weather_rate_sheet.get(weather_rate_id)
        if not weather_rate or not (0 < int(weather_rate[1 + 1]) < 100):
            continue

        place_list.append((
                get_idx(place_name_map, region),
                get_idx(place_name_map, name),
                get_idx(weather_rate_map, weather_rate_id),
                ))

    place_list = sorted(set(place_list))

    for weather_rate_id in range(len(weather_rate_map)):
        weather_rate = weather_rate_sheet.get(weather_rate_map[weather_rate_id])
        weather_rate_list.append((
                [get_idx(weather_name_map, int(weather_rate[x + 1])) for x in range(16)[0::2]],
                [int(weather_rate[x + 1]) for x in range(16)[1::2]],
                ))

    weather_sheet = load_dict_sheet('exd.ja/Weather.csv', 0, int)
    place_sheet = load_dict_sheet('exd.ja/PlaceName.csv', 0, int)

    lang_data = {
        'place': [x[0 + 1] for x in (place_sheet[i] for i in place_name_map)],
        'weather': [x[1 + 1] for x in (weather_sheet[i] for i in weather_name_map)],
        }

    # confilict check
    place_pairs = [(x, y) for (x, y, _) in place_list]
    for (x, y) in set(place_pairs):
        if place_pairs.count((x, y)) > 1:
            print ('conflicted place: ' + lang_data['place'][x] + ' ' + lang_data['place'][y])

    #  json.dump(lang_data, open('lang_data.json', 'w'))
    #  json.dump(place_list, open('place_list.json', 'w'))
    #  json.dump(weather_rate_list, open('weather_rate_list.json', 'w'))

    with open('data.js', 'w') as f:
        f.write('export default ' + json.dumps({
            'lang_data': lang_data,
            'place_list': place_list,
            'weather_rate_list': weather_rate_list,
            }))


if __name__ == '__main__':
    main()
