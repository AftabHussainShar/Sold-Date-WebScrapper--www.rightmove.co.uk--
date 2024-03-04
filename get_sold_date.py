import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

pd.options.display.max_columns = None
pd.options.display.width = 0
pd.options.display.max_colwidth = None


def get_property_details(rm_property_id):
    url = f'https://www.rightmove.co.uk/properties/{rm_property_id}?channel=RES_BUY'
    print(url)
    user_agent = {
    'authority': 'www.adultwork.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.adultwork.com',
    'referer': 'https://www.adultwork.com/Search.asp',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    property_details = requests.get(url, headers=user_agent)
    contents = property_details.content

    soup = BeautifulSoup(contents, features='html.parser')
    raw = soup.findAll('script')[5].text

    rm_property_details = raw.split('window.PAGE_MODEL = ')
    rm_property_details = rm_property_details[1]
    rm_property_details = json.loads(rm_property_details)

    df_property_details = pd.json_normalize(rm_property_details)
    df_extra_details = pd.DataFrame()
    df_extra_details['propertyId'] = df_property_details['propertyData.id']
    df_extra_details['Postcode'] = df_property_details['analyticsInfo.analyticsProperty.postcode']
    df_extra_details['UDPRN'] = df_property_details['propertyData.address.deliveryPointId']
    df_extra_details['Bedrooms'] = df_property_details['propertyData.bedrooms']
    df_extra_details['Bathrooms'] = df_property_details['propertyData.bathrooms']

    return df_extra_details

print(get_property_details(86140215))