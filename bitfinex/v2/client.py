#
# Example Bitfinex API v2 Auth Python Code
#
import requests  # pip install requests
import json
import hashlib
import hmac
import time

from datetime import datetime

START_TIME = time.mktime(datetime(2016, 1, 1).timetuple()) * 10000
END_TIME = time.time() * 10000


class Client(object):
    BASE_URL = "https://api.bitfinex.com/"

    def __init__(self, key, secret, use_pandas=False):
        self.KEY = key
        self.SECRET = secret
        self._use_pandas = use_pandas

        if use_pandas:
            global pandas
            import pandas

    def _nonce(self):
        return str(int(round(time.time() * 10000)))

    def _headers(self, path, nonce, body):
        secbytes = self.SECRET.encode(encoding='UTF-8')
        signature = "/api/" + path + nonce + body
        sigbytes = signature.encode(encoding='UTF-8')
        h = hmac.new(secbytes, sigbytes, hashlib.sha384)
        hexstring = h.hexdigest()
        return {
            "bfx-nonce": nonce,
            "bfx-apikey": self.KEY,
            "bfx-signature": hexstring,
            "content-type": "application/json"
        }

    def _parse_pandas(self, data, columns):
        df = pandas.DataFrame(data, columns=columns)
        df.drop(['_PLACEHOLDER'], inplace=True)
        return df

    def _convert_timestamps(self, df, columns):
        for col in columns:
            df[col] = pandas.to_datetime(df[col] * 1000000)

        return df

    def req(self, path, params={}):
        nonce = self._nonce()
        raw_body = json.dumps(params)
        headers = self._headers(path, nonce, raw_body)
        url = self.BASE_URL + path
        resp = requests.post(url, headers=headers, data=raw_body, verify=True)
        return resp

    def inactive_offers_history(self, symbol='fUSD', start=0, end=(time.time() * 10000), limit=1000):
        url = "v2/auth/r/funding/offers/{}/hist".format(symbol)
        params = {'start': start, 'end': end, limit: limit}
        response = self.req(url, params=params)
        columns = [
            'ID',
            'SYMBOL',
            'MTS_CREATED',
            'MTS_UPDATED',
            'AMOUNT',
            'AMOUNT_ORIG',
            'TYPE',
            '_PLACEHOLDER',
            '_PLACEHOLDER',
            'FLAGS',
            'STATUS',
            '_PLACEHOLDER',
            '_PLACEHOLDER',
            '_PLACEHOLDER',
            'RATE',
            'PERIOD',
            'NOTIFY',
            'HIDDEN',
            '_PLACEHOLDER',
            'RENEW',
            'RATE_REAL'
        ]
        data = response.json()

        if not self._use_pandas:
            return data

        df = self._parse_pandas(data, columns)
        df = self._convert_timestamps(df, ['MTS_CREATED', 'MTS_UPDATED'])
        return df

    def inactive_loans_history(self, symbol='fUSD', start=0, end=(time.time() * 10000), limit=1000):
        url = "v2/auth/r/funding/loans/{}/hist".format(symbol)

        params = {'start': start, 'end': end, limit: limit}
        response = self.req(url, params=params)
        columns = [
            'ID',
            'SYMBOL',
            'SIDE',
            'MTS_CREATE',
            'MTS_UPDATE',
            'AMOUNT',
            'FLAGS',
            'STATUS',
            '_PLACEHOLDER',
            '_PLACEHOLDER',
            '_PLACEHOLDER',
            'RATE',
            'PERIOD',
            'MTS_OPENING',
            'MTS_LAST_PAYOUT',
            'NOTIFY',
            'HIDDEN',
            '_PLACEHOLDER',
            'RENEW',
            'RATE_REAL',
            'NO_CLOSE',
        ]
        data = response.json()

        if not self._use_pandas:
            return data

        df = self._parse_pandas(data, columns)
        df = self._convert_timestamps(df, ['MTS_CREATE', 'MTS_UPDATE'])
        return df

    def funding_trades(self, symbol='fUSD', start=START_TIME, end=END_TIME, limit=250):
        url = "v2/auth/r/funding/trades/{}/hist".format(symbol)

        params = {'start': start, 'end': end, 'limit': limit}
        response = self.req(url, params=params)

        if response.status_code != 200:
            raise Exception(response.json())

        columns = [
            'ID',
            'CURRENCY',
            'MTS_CREATE',
            'OFFER_ID',
            'AMOUNT',
            'RATE',
            'PERIOD',
            'MAKER',
        ]
        data = response.json()

        if not self._use_pandas:
            return data

        df = self._parse_pandas(data, columns)
        df = self._convert_timestamps(df, ['MTS_CREATE'])
        return df
