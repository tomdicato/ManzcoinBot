import requests
import json
import pandas as pd
from flatten_json import flatten_json
import datetime

# get list of events by collection where a bid was entered
def get_collection_bids(slug = "manzcoin-nftz", event_type = "bid_entered", delay = 600):
    
    slug="manzcoin-nftz"
    event_type=event_type
    delay=delay

    # event_type="bid_entered"
    
    url="https://api.opensea.io/api/v1/events"

    collection_slug=slug
    
    delay=int(delay)    

    after=datetime.datetime.now() - datetime.timedelta(minutes=delay)

    after=after.timestamp()

    querystring={"collection_slug":str(collection_slug),"event_type":str(event_type),"occurred_after":after,"only_opensea":"false","offset":"0","limit":"200"}

    response=requests.request("GET", url, params=querystring)

    response_dict=json.loads(response.text)

    df = pd.DataFrame.from_dict(response_dict['asset_events'])    

    if len(df.index)==0:
        pass
    else:    

        df_asset=pd.DataFrame([flatten_json(x) for x in df['asset']])[['id','permalink','image_original_url','image_preview_url','image_thumbnail_url','name']]

        df_asset.rename(columns={'name':'asset_name'},inplace=True)
         
        df_bid_amount=pd.DataFrame(df['bid_amount'])
        
        df_bidder=pd.DataFrame([flatten_json(x) for x in df['from_account']])[['user_username']]

        df_bidder.rename(columns={'user_username':'bidder_username'},inplace=True)
        
        df_created_date=pd.DataFrame(df['created_date'])

        df_created_date.rename(columns={'created_date':'timestamp'},inplace=True)

        df_id=pd.DataFrame(df['id'])

        df_id.rename(columns={'id':'transaction_id'},inplace=True)

        df_bid_token=pd.DataFrame([flatten_json(x) for x in df['payment_token']])[['symbol','name','decimals','eth_price','usd_price']]
        
        manz_bidz=pd.concat([df[['collection_slug','event_type']],df_id,
        df_asset,df_bid_amount,df_bidder,df_created_date, df_bid_token], axis=1)        

        manz_bidz.sort_values(by=['timestamp'],ascending=False, inplace=True)

        manz_bidz['bid_amount'] = manz_bidz['bid_amount'].apply(lambda x: int(x)*0.000000000000000001)

        return manz_bidz

# manz_tranz = get_collection_sales(slug="manzcoin-nftz",event_type="successful",delay=5)