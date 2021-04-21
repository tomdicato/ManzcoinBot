from numpy import NaN
import requests
import json
import pandas as pd
from flatten_json import flatten_json
import datetime

# get list of events by collection
def get_collection_sales(slug = "manzcoin-nftz", event_type="successful", delay = 400):
    
    url="https://api.opensea.io/api/v1/events"

    slug="manzcoin-nftz"
    event_type="successful"
    delay=8000

    collection_slug=slug
    
    delay=int(delay)    

    after=datetime.datetime.now() - datetime.timedelta(minutes=delay)

    after=after.timestamp()

    querystring={"collection_slug":str(collection_slug),"event_type":str(event_type),"occurred_after":after,"only_opensea":"false","offset":"0","limit":"200"}

    response=requests.request("GET", url, params=querystring)

    if str(response.status_code)=="200":

        response_dict=json.loads(response.text)

        df = pd.DataFrame.from_dict(response_dict['asset_events'])

        if len(df.index)>0:

            df_asset=pd.DataFrame([flatten_json(x) for x in df['asset']])[['id','image_original_url','image_preview_url','image_thumbnail_url','name']]
            df_asset.rename(columns={'name':'asset_name'},inplace=True)

            df_seller=pd.DataFrame([flatten_json(x) for x in df['seller']])[['user_username','profile_img_url']]
            df_seller.rename(columns={'user_username':'seller_username','profile_img_url':'seller_profile_img_url'},inplace=True)
            
            df_buyer=pd.DataFrame([flatten_json(x) for x in df['winner_account']])[['user_username','profile_img_url']]
            df_buyer.rename(columns={'user_username':'buyer_username','profile_img_url':'buyer_profile_img_url'},inplace=True)

            df_transaction=pd.DataFrame([flatten_json(x) for x in df['transaction']])[['timestamp','id']]
            df_transaction.rename(columns={'id':'transaction_id'},inplace=True)            

            df_token=pd.DataFrame([flatten_json(x) for x in df['payment_token']])[['symbol']]

            df_total_price=df['total_price'].apply(lambda x: int(x)*0.000000000000000001)

            manz_tranz=pd.concat([df[['collection_slug','event_type']],df_total_price,df_token,df_asset,df_buyer,df_seller,df_transaction], axis=1)
                        
            manz_tranz.sort_values(by=['timestamp'],ascending=False, inplace=True)

            return manz_tranz
            
        else:
            return "No data returned"

    else:
        return f"Oops! response status code:{ response.status_code })"

manz_tranz = get_collection_sales(slug="manzcoin-nftz",event_type="successful",delay=8000)