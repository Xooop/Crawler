import requests

proxies = {"http": "127.0.0.1:1080", "https": "127.0.0.1:1080"}


def func1():
    url = 'http://spys.ru/free-proxy-list/IE'
    response = requests.get(url, proxies=proxies)
    raw = response.text
    dic = {'Four6EightOne^Zero1Nine': 1,
           'SevenOneOneSeven^FiveEightTwo': 2,
           'Five3TwoThree^Seven3Six': 3,
           'FourNineThreeTwo^FourEightSeven': 4,
           'Eight2ZeroNine^ThreeThreeThree': 5,
           'One4SevenFive^Three6One': 6,
           'OneTwoFiveSix^Five1Zero': 7,
           'Eight4SixZero^Four0Five': 8,
           'EightEightFourEight^Zero9Four': 9,
           'NineSixNineFour^SevenOneEight': 0}
    regex_ip = 'spy14>(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})<'
    regex_port = ''


if __name__ == '__main__':
    print(860 ^ 405)
