import logging
from pandas.core.reshape.concat import concat
from config import create_api
import time
from get_collection import get_collection_sales
from get_collection_bids import get_collection_bids
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_for_sales(api, delay, filename):

    logger.info("Retreiving sales")
    
    manz_tranz = get_collection_sales(slug="manzcoin-nftz",event_type="successful",delay=delay)
    manz_bidz = get_collection_bids(slug = "manzcoin-nftz", event_type="bid_entered", delay=delay)

    if manz_tranz is not None:

        manz_tranz_existing = pd.read_csv('manz_tranz_list.csv')
    
        for i in range(len(manz_tranz)):

            if manz_tranz['transaction_id'][i] not in manz_tranz_existing['transaction_id'].values:
            
                price = manz_tranz['total_price'][i]
                seller = manz_tranz['seller_username'][i]
                buyer = manz_tranz['buyer_username'][i]
                asset_name=manz_tranz['asset_name'][i]

                nl = '\n'       

                status_string = f"{asset_name} SOLD!{nl}From: {seller}{nl}To: {buyer}{nl}For: {price}{nl}#MANZCOIN"

                api.update_with_media(
                    filename = filename,
                    status = status_string
                    )

                manz_tranz[['transaction_id','timestamp']].head(i+1).to_csv('manz_tranz_list.csv', mode='a', index=False, header=False)

    if manz_bidz is not None:

        manz_tranz_existing = pd.read_csv('manz_tranz_list.csv')
        i=0
    
        for i in range(len(manz_bidz)):

            if manz_bidz['transaction_id'][i] not in manz_tranz_existing['transaction_id'].values:
            
                bid_amount=manz_bidz['bid_amount'][i]
                bidder=manz_bidz['bidder_username'][i]
                symbol=manz_bidz['symbol'][i]
                asset_name=manz_bidz['asset_name'][i]
                asset_permalink=manz_bidz['permalink'][i]

                nl = '\n'       

                status_string = (f"MANZ COIN BID INCREASED!{nl}From: { bidder }{nl}For: "
                f"{ bid_amount } { symbol }{nl}{asset_permalink}{nl}#MANZCOIN")

                api.update_with_media(
                    filename = filename,
                    status = status_string
                    )

                manz_bidz[['transaction_id','timestamp']].head(i+1).to_csv('manz_tranz_list.csv', mode='a', index=False, header=False)

def main():
    api = create_api()
    delay = 330
    filename = "data/ManzCoin.gif"    
    check_for_sales(api, delay, filename)

if __name__ == "__main__":
    main()