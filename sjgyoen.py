import cotohappy
import requests
from bs4 import BeautifulSoup


def get_kotonoha_story():

    url = 'https://www.kotonohanoniwa.jp/page/product.html'
    res = requests.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    p = soup.find_all('p', class_='mb24')[-1]

    return p.text


if __name__ == '__main__':

    coy = cotohappy.API()

    """ getting parse """
    print('\n#### parse origin ####')
    sentence = get_kotonoha_story()
    kuzure   = False
    parse_li = coy.parse(sentence, kuzure)
    for parse in parse_li:
        print(parse)

    print(parse.key_name)

    """ getting tokens; it is a little more difficult than MeCab Janome """
    print('\n#### parse tokens ####')
    for parse in parse_li:
        for token in parse.tokens:
            print(token)

    print(token.key_name)

    """ if you extract just nouns, you write: """
    print('\n#### extract nouns ####')
    nouns: [str] = []
    for parse in parse_li:
        for token in parse.tokens:
            if token.pos == '名詞':
                nouns.append(token.form)

    print(nouns)
