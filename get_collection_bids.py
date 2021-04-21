import requests
import json
import pandas as pd
from flatten_json import flatten_json
import datetime

# get list of events by collection where a bid was entered
def get_collection_bids(slug="manzcoin-nftz", event_type="bid_entered", delay = 6000):
      
    url="https://api.opensea.io/api/v1/events"

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

            df_asset=pd.DataFrame([flatten_json(x) for x in df['asset']])[
                ['id','permalink','image_original_url','image_preview_url','image_thumbnail_url','name']].rename(
                    columns={'name':'asset_name'},inplace=True)                        

            df_bid_amount=df['bid_amount'].apply(
                lambda x: int(x)*0.000000000000000001).to_frame()

            df_bidder=pd.DataFrame([flatten_json(x) for x in df['from_account']])[
                ['user']].rename(columns={'user':'bidder_username'})            

            df_created_date=df['created_date'].to_frame()
            
            df_created_date.rename(columns={'created_date':'timestamp'},inplace=True)

            df_id=df['id'].to_frame().rename(columns={'id':'transaction_id'})            

            df_bid_token=pd.DataFrame([flatten_json(x) for x in df['payment_token']])[
                ['symbol','name','decimals','eth_price','usd_price']]

            manz_bidz=pd.concat([df[['collection_slug','event_type']],
                df_id, df_asset,df_bid_amount,df_bidder,df_created_date, df_bid_token], axis=1)

            manz_bidz=manz_bidz.sort_values(by=['timestamp'],ascending=True)
            
            return manz_bidz

        else:
            return "No data returned"

    else:
        return f"Oops! response status code:{ response.status_code })"

# manz_tranz = get_collection_bids(slug="manzcoin-nftz",event_type="bid_entered",delay=60000)

