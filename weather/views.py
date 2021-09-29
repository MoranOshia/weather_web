# Editor: Moran Oshia

from bs4 import BeautifulSoup
from django.shortcuts import render
from urllib.request import Request, urlopen


def data_filter(content, ident, offset, stop):
    """
    This function return the result of the html
    by scraping in the html
    base on the relevant data it gets:
    content: url data
    ident: the id of the element in the html
    offset and stop : relevant indexs
    """

    position = content.find(ident)

    data = content[position + offset:position + offset + 50]

    result = ''

    for x in range(len(data)):
        testData = data[x:x + 1]
        if testData == stop:
            break
        result += data[x:x + 1]

    return result


def get_html_jer_nyc():
    """
    This function return the content of jerusalem an nyc
    by scraping to the html of google search weather
    """

    req_jer = Request('https://www.google.com/search?q=weather+jerusalem')
    req_jer.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.3')
    content_jer = urlopen(req_jer).read().decode("utf8")

    req_nyc = Request('https://www.google.com/search?q=weather+' + 'new+york')
    req_nyc.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.3')
    content_nyc = urlopen(req_nyc).read().decode("utf8")

    return content_jer, content_nyc


def get_html_content(request):
    """
    This function return the content of the search city by the user
    by scraping to the html of google search weather
    """

    # get the city the user entered from the html
    city = request.GET.get('city')
    city = city.replace(" ", "+")

    # scraping into the google weather sreach
    req = Request('https://www.google.com/search?q=weather+' + city)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.3')
    content = urlopen(req).read().decode("utf8")
    return content


def get_data_from_html(content):
    """
    This function return data  and the image url of the weather by the content
    in the list it will holds: temperature, humidity, wind, rain, sky, location, time
    """
    # city weather data
    temperature = data_filter(content, 'id="wob_tm"', 35, '<')
    humidity = data_filter(content, 'id="wob_hm"', 12, '%')
    wind = data_filter(content, 'id="wob_ws"', 12, ' ')
    rain = data_filter(content, 'id="wob_pp"', 12, '%')
    sky = data_filter(content, 'id="wob_dc"', 12, '<')
    location = data_filter(content, 'id="wob_loc"', 13, '<')
    time = data_filter(content, 'id="wob_dts"', 13, '<')

    # city url of the image weather status
    s = content.find("class=" + "\"wob_tci\"")
    pic_url_start = content.find("src", s)
    pic_url_end = content.find("id", s)
    pic_url = content[pic_url_start + 5:pic_url_end - 2]


    #soup = BeautifulSoup('core/home.html')
    #for img in soup.findAll('img'):
       # img['src'] = pic_url

    l = [temperature, humidity, wind, rain, sky, location, time]
    return l, pic_url


def home(request):
    """
    This function return the render
    send to the home page the elements
    """

    search_data = None
    result = None
    pic_url = ""
    flag = True

    # data for Jerusalem and Nyc
    content_ta, content_nyc = get_html_jer_nyc()
    data_jer, pic_url_jer = get_data_from_html(content_ta)
    data_nyc, pic_url_nyc = get_data_from_html(content_nyc)

    if 'city' in request.GET:

        # html data of the searched city
        content = get_html_content(request)

        # searched city weather data
        temperature = data_filter(content, 'id="wob_tm"', 35, '<')
        humidity = data_filter(content, 'id="wob_hm"', 12, '%')
        wind = data_filter(content, 'id="wob_ws"', 12, ' ')
        rain = data_filter(content, 'id="wob_pp"', 12, '%')
        sky = data_filter(content, 'id="wob_dc"', 12, '<')
        location = data_filter(content, 'id="wob_loc"', 13, '<')
        time = data_filter(content, 'id="wob_dts"', 13, '<')

        # searched city url of the image weather status
        s = content.find("class=" + "\"wob_tci\"")
        pic_url_start = content.find("src", s)
        pic_url_end = content.find("id", s)
        pic_url = content[pic_url_start + 5:pic_url_end - 2]

        # check if the city entered by the user is correct
        if time == "ml>":
            flag = False

        search_data = [temperature, humidity, wind, rain, sky, location, time]

    return render(request, 'weather/home.html',
                  {'result': search_data, 'nycData': data_nyc, 'picnyc': pic_url_nyc, 'taData': data_jer,
                   'picta': pic_url_jer, 'pic': pic_url, 'flag': flag})
