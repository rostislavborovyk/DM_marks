import urllib.request
from bs4 import BeautifulSoup
import sys
import re
import time
import pandas as pd


def get_html_from_novotar():
    password = 'KPI_2019'
    username = 'student_fict'
    url = 'http://amodm.pp.ua'
    passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    authhndler = urllib.request.HTTPBasicAuthHandler(passman)
    opener = urllib.request.build_opener(authhndler)
    urllib.request.install_opener(opener)
    html = urllib.request.urlopen(url)
    return html


def get_html(url):
    response = urllib.request.urlopen(url)
    return response


def get_urls_of_groups_marks(html):
    soup = BeautifulSoup(html, features="html.parser")
    urls = soup.find('div', id='fragment-37')
    urls = urls.find_all('a')[:6]
    pattern = re.compile('href=".+"')
    hrefs = list((re.search(pattern, str(i)).group(0)[6:-1] for i in urls))
    return hrefs


def information_from_group(url_of_group, num):
    html = get_html(url_of_group)
    soup = BeautifulSoup(html, features="html.parser")
    table = soup.find_all('table', class_='waffle')
    table = table[num]
    rows = table.find_all('tr')
    names_of_columns = rows[2].find_all('td')
    columns_for_df = [i.text for i in names_of_columns][1:]

    name_of_group = rows[1].find_all('td')[1].text
    print("Now is: ", name_of_group)


    columns_for_df.append('Група')
    df = pd.DataFrame(columns=columns_for_df)
    correction = df.shape[0]
    for index in range(1, len(rows)):
        if str(rows[index].find_all('td')[0].text).isdecimal():
            row_inf = [rows[index].find_all('td')[i].text for i in range(1, df.shape[1])]
            row_inf.append(name_of_group)
            df.loc[index+correction-3] = row_inf
    df.to_excel(name_of_group + '.xls')


def main():
    start = time.time()
    ls_of_links = get_urls_of_groups_marks(get_html_from_novotar())
    for i in range(len(ls_of_links)):
        information_from_group(ls_of_links[i], i)
    print("Time spent: {:.3f} seconds".format(time.time() - start))


if __name__ == '__main__':
    main()

