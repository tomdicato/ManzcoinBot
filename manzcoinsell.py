import logging
from config import create_api
from update_github_file import updatefilefromgithub
from get_collection_sales import get_collection_sales
from get_collection_bids import get_collection_bids
from read_github_csv import read_csv_from_github
import os
import pandas as pd
import numpy as np

gh_access_token = os.environ.get("MANZCOIN_GITHUB_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_for_sales(api, delay, filename):

    logger.info("Retreiving sales")

    manz_tranz = get_collection_sales(
        slug="manzcoin-nftz", event_type="successful", delay=delay
    )

    # manz_bidz = get_collection_bids(slug = "manzcoin-nftz", event_type="bid_entered", delay=delay)

    if manz_tranz != "No data returned":

        manz_tranz_existing = read_csv_from_github(
            repo_name="ManzcoinBot",
            git_file="manz_tranz_list.csv",
            repo_owner="tomdicato",
            branch="main",
        )

        # find transactions that haven't been processed before
        manz_tranz_filter = manz_tranz[
            ~manz_tranz.transaction_id.isin(manz_tranz_existing.transaction_id.values)
        ].copy()

        nl = "\n"

        j = 0

        manz_tranz_filter["status_string"] = (
            manz_tranz_filter["asset_name"].astype(str) + " NFTz SOLD!\n"
            "From: " + manz_tranz_filter["seller_username"].astype(str) + "\n"
            "To: " + manz_tranz_filter["buyer_username"].astype(str) + "\n"
            "For: "
            + manz_tranz_filter["total_price"].astype(str)
            + " "
            + manz_tranz_filter["symbol"].astype(str)
            + "\n"
            "#MANZCOIN" + "\n"
            "https://opensea.io/collection/manzcoin-nftz"
        )

        manz_tranz_filter.apply(
            lambda x: api.update_with_media(filename=filename, status=x.status_string),
            axis=1,
        )

        # api.update_with_media(
        #     filename=filename,
        #     status=status_string
        #     )

        j += 1

        updatefilefromgithub(
            gh_access_token,
            repo_name="ManzcoinBot",
            git_file="manz_tranz_list.csv",
            repo_owner="tomdicato",
            branch="main",
            new_tweets=manz_tranz_filter,
            message=f"updated {j} transactions",
        )

    # if manz_bidz is not None:

    #     manz_tranz_existing = read_csv_from_github(repo_name='ManzcoinBot', git_file = 'manz_tranz_list.csv', repo_owner='tomdicato', branch='main')

    #     j=0

    #     for i in range(len(manz_bidz)):

    #         if manz_bidz['transaction_id'][i] not in manz_tranz_existing['transaction_id'].values:

    #             bid_amount=manz_bidz['bid_amount'][i]
    #             bidder=manz_bidz['bidder_username'][i]
    #             symbol=manz_bidz['symbol'][i]
    #             asset_name=manz_bidz['asset_name'][i]
    #             asset_permalink=manz_bidz['permalink'][i]

    #             nl = '\n'

    #             status_string = (f"MANZCOIN NFTz BID INCREASED!{nl}From: { bidder }{nl}For: "
    #             f"{ bid_amount } { symbol }{nl}{asset_permalink}{nl}#MANZCOIN")

    #             api.update_with_media(
    #                 filename = filename,
    #                 status = status_string
    #                 )

    #             j+=1

    #     updatefilefromgithub(gh_access_token, repo_name='ManzcoinBot',
    #         git_file = 'manz_tranz_list.csv',repo_owner='tomdicato', branch='main', new_tweets=manz_bidz, message=f"updated {j} bids")


def main():
    api = create_api()
    delay = 8000
    filename = "data/ManzCoin.gif"
    check_for_sales(api, delay, filename)


if __name__ == "__main__":
    main()