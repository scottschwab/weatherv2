import requests_mock
import requests
import pull_weather
import os

def setUp():
    os.environ.putenv("API_KEY","aaaaaaaa")
    os.environ.putenv("AWS_REGION", "us-west-2")
    os.environ.putenv("QUEUE_NAME", "randy")
    
def test_good_pull():
    msg = pull_weather.get_bbox(30,-98,28,-97,10)
    assert msg == "bbox=-98,30,-97,28,10"

def test_s_n_pull():
    try:
        msg = pull_weather.get_bbox(20,-98,28,-97,10)
    except ValueError as v:
        if str(v).index("north") < 0:
            raise False
        assert True
        return
    assert False 

def test_e_w_pull():
    try:
        msg = pull_weather.get_bbox(30,-20, 28,-97,10)
    except ValueError as v:
        if str(v).index("west") < 0:
            raise False
        assert True
        return
    assert False 

def test_scale():
    try:
        msg = pull_weather.get_bbox(30,-98, 28,-97,0)
    except ValueError as v:
        if str(v).index("positive") < 0:
            raise False
        assert True
        return
    assert False

def test__get_api():

    assert pull_weather.get_appid() == f"APPID={pull_weather.API_KEY}"

def test_get_path():
    assert pull_weather.get_path(30,-98,28,-97,10).index(pull_weather.REQUEST_PATH + "?") > -1

def test_request():
    """
    TODO: get mock request working!
    """
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount('mock',adapter)
    adapter.register_uri(f"http://{pull_weather.HOST}", valid_data)
    r = pull_weather.pull(30,-98,28,-97,10)
    print(len(r))


valid_data = """
{
"cod": 200,
"calctime": 0.135811114,
"cnt": 31,
"list": [
{
"id": 4232679,
"dt": 1560517624,
"name": "Alton",
"coord": {
"Lon": -90.18,
"Lat": 38.89
},
"main": {
"temp": 15.88,
"temp_min": 13,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 63
},
"visibility": 16093,
"wind": {
"speed": 4.6,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4234969,
"dt": 1560517624,
"name": "Cahokia",
"coord": {
"Lon": -90.19,
"Lat": 38.57
},
"main": {
"temp": 15.86,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1021,
"humidity": 82
},
"visibility": 16093,
"wind": {
"speed": 2.1,
"deg": 160
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4239714,
"dt": 1560517624,
"name": "Granite City",
"coord": {
"Lon": -90.15,
"Lat": 38.7
},
"main": {
"temp": 15.96,
"temp_min": 13,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 63
},
"visibility": 16093,
"wind": {
"speed": 4.6,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4241704,
"dt": 1560517624,
"name": "Jacksonville",
"coord": {
"Lon": -90.23,
"Lat": 39.73
},
"main": {
"temp": 16.47,
"temp_min": 14,
"temp_max": 17.78,
"pressure": 1019,
"humidity": 59
},
"visibility": 16093,
"wind": {
"speed": 4.6,
"deg": 180
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4237579,
"dt": 1560517624,
"name": "East Saint Louis",
"coord": {
"Lon": -90.15,
"Lat": 38.62
},
"main": {
"temp": 15.88,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1021,
"humidity": 82
},
"visibility": 16093,
"wind": {
"speed": 2.1,
"deg": 160
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4239509,
"dt": 1560517624,
"name": "Godfrey",
"coord": {
"Lon": -90.19,
"Lat": 38.96
},
"main": {
"temp": 15.85,
"temp_min": 13,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 63
},
"visibility": 16093,
"wind": {
"speed": 4.6,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4251841,
"dt": 1560517629,
"name": "Upper Alton",
"coord": {
"Lon": -90.15,
"Lat": 38.91
},
"main": {
"temp": 15.89,
"temp_min": 13,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 63
},
"visibility": 16093,
"wind": {
"speed": 4.6,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4374513,
"dt": 1560517629,
"name": "Affton",
"coord": {
"Lon": -90.33,
"Lat": 38.55
},
"main": {
"temp": 15.83,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 82
},
"visibility": 16093,
"wind": {
"speed": 2.1,
"deg": 140
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4375663,
"dt": 1560517629,
"name": "Ballwin",
"coord": {
"Lon": -90.55,
"Lat": 38.6
},
"main": {
"temp": 15.76,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 71
},
"visibility": 16093,
"wind": {
"speed": 3.1,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4381072,
"dt": 1560517629,
"name": "Chesterfield",
"coord": {
"Lon": -90.58,
"Lat": 38.66
},
"main": {
"temp": 15.76,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 71
},
"visibility": 16093,
"wind": {
"speed": 3.1,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4381478,
"dt": 1560517629,
"name": "Clayton",
"coord": {
"Lon": -90.32,
"Lat": 38.64
},
"main": {
"temp": 15.83,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 59
},
"visibility": 16093,
"wind": {
"speed": 3.6,
"deg": 190
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4382837,
"dt": 1560517629,
"name": "Creve Coeur",
"coord": {
"Lon": -90.42,
"Lat": 38.66
},
"main": {
"temp": 15.74,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 59
},
"visibility": 16093,
"wind": {
"speed": 3.6,
"deg": 190
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4386387,
"dt": 1560517629,
"name": "Ferguson",
"coord": {
"Lon": -90.31,
"Lat": 38.74
},
"main": {
"temp": 15.83,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 59
},
"visibility": 16093,
"wind": {
"speed": 3.6,
"deg": 190
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4382072,
"dt": 1560517629,
"name": "Concord",
"coord": {
"Lon": -90.36,
"Lat": 38.52
},
"main": {
"temp": 15.8,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 82
},
"visibility": 16093,
"wind": {
"speed": 2.1,
"deg": 140
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4386802,
"dt": 1560517629,
"name": "Florissant",
"coord": {
"Lon": -90.32,
"Lat": 38.79
},
"main": {
"temp": 15.87,
"temp_min": 13,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 63
},
"visibility": 16093,
"wind": {
"speed": 4.6,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4389967,
"dt": 1560517629,
"name": "Hazelwood",
"coord": {
"Lon": -90.37,
"Lat": 38.77
},
"main": {
"temp": 15.7,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 59
},
"visibility": 16093,
"wind": {
"speed": 3.6,
"deg": 190
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4401242,
"dt": 1560517629,
"name": "OFallon",
"coord": {
"Lon": -90.7,
"Lat": 38.81
},
"main": {
"temp": 15.76,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 71
},
"visibility": 16093,
"wind": {
"speed": 3.1,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4397962,
"dt": 1560517629,
"name": "Mehlville",
"coord": {
"Lon": -90.32,
"Lat": 38.51
},
"main": {
"temp": 15.83,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1021,
"humidity": 82
},
"visibility": 16093,
"wind": {
"speed": 2.1,
"deg": 160
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4396915,
"dt": 1560517629,
"name": "Manchester",
"coord": {
"Lon": -90.51,
"Lat": 38.6
},
"main": {
"temp": 15.76,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 71
},
"visibility": 16093,
"wind": {
"speed": 3.1,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4402178,
"dt": 1560517629,
"name": "Overland",
"coord": {
"Lon": -90.36,
"Lat": 38.7
},
"main": {
"temp": 15.78,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 59
},
"visibility": 16093,
"wind": {
"speed": 3.6,
"deg": 190
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4397340,
"dt": 1560517629,
"name": "Maryland Heights",
"coord": {
"Lon": -90.43,
"Lat": 38.71
},
"main": {
"temp": 15.74,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 59
},
"visibility": 16093,
"wind": {
"speed": 3.6,
"deg": 190
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4393739,
"dt": 1560517629,
"name": "Kirkwood",
"coord": {
"Lon": -90.41,
"Lat": 38.58
},
"main": {
"temp": 15.78,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 71
},
"visibility": 16093,
"wind": {
"speed": 3.1,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4394905,
"dt": 1560517629,
"name": "Lemay",
"coord": {
"Lon": -90.28,
"Lat": 38.53
},
"main": {
"temp": 15.83,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1021,
"humidity": 82
},
"visibility": 16093,
"wind": {
"speed": 2.1,
"deg": 160
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4407237,
"dt": 1560517629,
"name": "Saint Peters",
"coord": {
"Lon": -90.63,
"Lat": 38.8
},
"main": {
"temp": 15.79,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 71
},
"visibility": 16093,
"wind": {
"speed": 3.1,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4407066,
"dt": 1560517629,
"name": "Saint Louis",
"coord": {
"Lon": -90.2,
"Lat": 38.63
},
"main": {
"temp": 15.83,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1021,
"humidity": 82
},
"visibility": 16093,
"wind": {
"speed": 2.1,
"deg": 160
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4409591,
"dt": 1560517629,
"name": "Spanish Lake",
"coord": {
"Lon": -90.22,
"Lat": 38.79
},
"main": {
"temp": 15.96,
"temp_min": 13,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 63
},
"visibility": 16093,
"wind": {
"speed": 4.6,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4406831,
"dt": 1560517629,
"name": "Saint Charles",
"coord": {
"Lon": -90.48,
"Lat": 38.78
},
"main": {
"temp": 15.72,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 59
},
"visibility": 16093,
"wind": {
"speed": 3.6,
"deg": 190
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4413872,
"dt": 1560517629,
"name": "Webster Groves",
"coord": {
"Lon": -90.36,
"Lat": 38.59
},
"main": {
"temp": 15.8,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 82
},
"visibility": 16093,
"wind": {
"speed": 2.1,
"deg": 140
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4412697,
"dt": 1560517629,
"name": "University City",
"coord": {
"Lon": -90.31,
"Lat": 38.66
},
"main": {
"temp": 15.83,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 59
},
"visibility": 16093,
"wind": {
"speed": 3.6,
"deg": 190
},
"rain": null,
"snow": null,
"clouds": {
"today": 40
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
]
},
{
"id": 4414749,
"dt": 1560517629,
"name": "Wildwood",
"coord": {
"Lon": -90.66,
"Lat": 38.58
},
"main": {
"temp": 15.79,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 71
},
"visibility": 16093,
"wind": {
"speed": 3.1,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
},
{
"id": 4414001,
"dt": 1560517629,
"name": "Wentzville",
"coord": {
"Lon": -90.85,
"Lat": 38.81
},
"main": {
"temp": 15.58,
"temp_min": 12.78,
"temp_max": 18.33,
"pressure": 1020,
"humidity": 71
},
"visibility": 16093,
"wind": {
"speed": 3.1,
"deg": 170
},
"rain": null,
"snow": null,
"clouds": {
"today": 1
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
]
}
]
}
"""