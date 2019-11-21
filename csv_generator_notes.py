import requests
import pandas as pd
import io


def get_finance_data(assets, start_date, end_date):

    finance_data = pd.DataFrame()
    for i, asset in enumerate(assets):
        host = 'http://stooq.com/'

        url = f'http://stooq.com/q/d/l/?s={asset}&d1={start_date}&d2={end_date}/{asset}.csv'
        print(url)
        try:
            response = requests.get(url)
        except Exception as e:
            raise Exception(f'{e.__class__.__name__}: {e}')
        if response.ok:
            decoded_content = response.content.decode('utf-8')
            if i == 0:
                finance_data['Date'] = \
                    pd.read_csv(io.StringIO(decoded_content))['Date']
            finance_data[asset.upper()] = \
                pd.read_csv(io.StringIO(decoded_content))['Close']
        else:
            raise Exception(f'Could not retrieve data:{response.status_code}')
    
    return finance_data


if __name__ == '__main__':

    assets = ['btc.v', 'eth.v', 'dash.v', 'bch.v', 'ltc.v', 'xrp.v', 'xmr.v', 'zec.v']
    start_date = int('2018' + '01' + '01')
    end_date = int('2019' + '11' + '05')

    finance_data = get_finance_data(assets, start_date, end_date)
    # print(finance_data)
    print(finance_data.tail())
    assets = "-".join(assets)
    finance_data.to_csv(f'{assets}.csv', index=False)
