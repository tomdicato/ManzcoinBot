import logging
from bots.config import create_api
import time
from get_collection import get_collection_sales
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_for_sales(api, delay, filename):
    logger.info("Retreiving sales")
    
    manz_tranz = get_collection_sales(slug="manzcoin-nftz",event_type="successful",delay=delay)

    manz_tranz_existing = pd.read_csv('manz_tranz_list.csv')
    
    for i in range(len(manz_tranz)):

        if manz_tranz['transaction_id'][i] not in manz_tranz_existing['transaction_id'].values:
            
            price = manz_tranz['total_price'][i]
            seller = manz_tranz['seller_username'][i]
            buyer = manz_tranz['buyer_username'][i]

            nl = '\n'       

            status_string = f"MANZ COIN SOLD!{nl}From: {seller}{nl}To: {buyer}{nl}For: {price}{nl}Feels cute might delete. #MANZCOIN"
        
            api.update_with_media(
                filename = filename,
                status = status_string
                )
                
            manz_tranz[['transaction_id','timestamp']].head(i+1).to_csv('manz_tranz_list.csv', mode='a', index=False, header=False)

def main():
    api = create_api()
    delay = 300
    filename = "data/ManzCoin.gif"
    while True:
        check_for_sales(api, delay, filename)
        logger.info("Waiting...")
        time.sleep(300)

if __name__ == "__main__":
    main()