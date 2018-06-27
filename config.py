# -*- coding: utf-8 -*-
#COM Object DLL
SKCOMDLL = 'C:\\capital\\CapitalAPI_2.13.12\\API\\x86\\SKCOM.dll'
SKLogPath = './Logs'

#History Path
HistoryPath = './history/'
CachePath = HistoryPath + 'cache'
StocksPath = HistoryPath + 'stocks'

#warrant
WarrantBaseURL = 'http://iwarrant.capital.com.tw/wdataV2/canonical/capital-newvol/%E6%AC%8A%E8%AD%89%E9%81%94%E4%BA%BA%E5%AF%B6%E5%85%B8_NEWVOL_'
WarrantBaseFilename = 'warrant_NEWVOL_'
WarrantPath = HistoryPath + 'warrant'

#Staock label
KLFIELD = ['Date','Open','High','Low','Close','Volume']
KLFIELDTYPES = {'Date': str, 'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': int}

WFIELD = ['Code', 'Name', 'Vendor', 'Cost', 'Fluctuation', 'F-Percent', 'Volumn', 'Buy', 'Sell', 'Spread', 'Premium',
        'IOTM', 'Theoretical', 'IV', 'Leverage', 'Remainder', 'ExerciseRatio', 'Stock', 'StockName', 'StockCost',
        'StockFluctuation', 'SF-Percent','Exercise', 'Boundary', 'SVolatility20', 'SVolatility60', 'SVolatility120', 'Delta',
        'Gamma', 'Vega', 'Theta', 'EV', 'TV', 'OutstandingShares', 'OS-Variation', 'ListingDay', 'Expiration',
        'TotalVolumn', 'OfferPrice', 'Type']
WTFIELD = ['Code', 'Name', 'Vendor', 'Cost', 'Fluctuation', 'F-Percent', 'Volumn', 'Buy', 'Sell', 'Spread', 'Premium',
        'IOTM', 'Theoretical', 'IV', 'Leverage', 'Remainder', 'ExerciseRatio', 'Stock', 'StockName', 'StockCost',
        'StockFluctuation', 'SF-Percent','Exercise', 'Boundary', 'SVolatility20', 'SVolatility60', 'SVolatility120', 'Delta',
        'Gamma', 'Vega', 'Theta', 'EV', 'TV', 'OutstandingShares', 'OS-Variation', 'ListingDay', 'Expiration',
        'TotalVolumn', 'OfferPrice', 'Type','Date']

WTFIELDTYPES = {'Code': str, 'Name': str, 'Vendor': str, 'Cost': float,
        'Fluctuation': float, 'F-Percent': float, 'Volumn': int, 'Buy':float,
        'Sell':float, 'Spread': float, 'Premium': float, 'IOTM': float, 'Theoretical': float, 'IV': float, 'Leverage': float,
        'Remainder': int, 'ExerciseRatio': float, 'Stock': str, 'StockName':
        str, 'StockCost': float,
        'StockFluctuation': float, 'SF-Percent': float,'Exercise': float,
        'Boundary': str, 'SVolatility20': float, 'SVolatility60': float,
        'SVolatility120': float, 'Delta': float,
        'Gamma': float, 'Vega': float, 'Theta': float, 'EV': float, 'TV':
        float, 'OutstandingShares': int, 'OS-Variation': int, 'ListingDay':
        str, 'Expiration': str, 'TotalVolumn': int, 'OfferPrice': float,
        'Type': str, 'Date': str}
