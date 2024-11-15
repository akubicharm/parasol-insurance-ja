import requests
import os
import json

import logging
from dotenv import dotenv_values, load_dotenv

from llm_usage import infer_with_template
import db_utils

# Initialize logger
logger = logging.getLogger("app")

# Get config
config = {
    **dotenv_values(".env"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
    **dotenv_values(".pipeline-envs"), # load pipeline-specific vars
}

db = db_utils.Database(config, logger)

def upload_sentiment(claim_id, sentiment):
    db.update_claim_sentiment(claim_id, sentiment)

def get_claim_sentiment(claim_id = None):    
    claim_info = db.get_claim_info(claim_id)
    claim_body = claim_info["body"]
    
    with open('templates/system_template.txt') as f:
        system_template = f.read()

    with open('templates/sentiment_template.txt') as f:
        user_template = f.read()
    
    sentiment = infer_with_template(claim_body, system_template, user_template)
    print(sentiment)
    upload_sentiment(claim_id, sentiment)
    
    
def batch_get_claim_sentiment(claim_ids = None):
    if not claim_ids:
        with open('claims.json') as f:
            claim_ids = json.load(f)["claim_ids"]
                
    print(f"processing claims: {claim_ids}")
    
    for claim_id in claim_ids:
        get_claim_sentiment(claim_id)
    
if __name__ == '__main__':
    sentiment = batch_get_claim_sentiment()