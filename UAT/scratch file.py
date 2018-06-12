import bs4 as bs
import requests


def get_source_code(url, mod_header=False):
    if mod_header:
        headers = {'v2header': 'true'}
        request = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(request.text, "lxml")
    else:
        request = requests.get(url)
        soup = bs.BeautifulSoup(request.text, "lxml")

        history = request.history
        history_list = [str(h) for h in history]
        if '<Response [301]>' in history_list:
            if 'confirmation' in url:
                print('this is a confirmation page and was redirected to Reg page O.o ')

    return soup

adobe = get_source_code('https://www.solarwinds.com/network-bandwidth-analyzer-pack/confirmation')


