# -*- coding: utf-8 -*-
import datetime
import requests

baseurl = 'http://iwarrant.capital.com.tw/wdataV2/canonical/capital-newvol/%E6%AC%8A%E8%AD%89%E9%81%94%E4%BA%BA%E5%AF%B6%E5%85%B8_NEWVOL_'
basefilename = '權證達人寶典_NEWVOL_'

if __name__ == '__main__':
    date =  datetime.datetime.now().strftime("%Y-%m-%d")
    print('Today is %s' % date)

    url = baseurl + date + '.xls'
    filename = basefilename + date + '.xls'

    print('Start to getting the xls file')
    res = requests.get(url)

    if res.status_code is not 200:
        print('Get File Error ...')
        exit(0)

    print('Get File OK')

    fp = open(filename, 'wb')

    with open(filename, 'wb') as xls:
        xls.write(res.content)
    





