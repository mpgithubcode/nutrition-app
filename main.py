import os
import requests
import dotenv
import logging
import json
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(name)s: %(message)s")
file_handler = logging.FileHandler('meal_planner.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

fdcId = "dick"

dotenv.load_dotenv()
api_key = os.getenv('API_KEY')
host, endp, one_food_endp = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}", "&query=", f"/v1/food/{fdcId}"

def search_foods(query):
    logger.debug("query_database() function called")
    logger.debug(f"URL --> {host}")
    logger.debug(f"METHOD --> POST")
    logger.debug(f"QUERY --> {query}")
    
    headers = {"Content-Type": "application/json"}

    try:
            response = requests.post(host, headers=headers, data=json.dumps(query))
    
            logger.info(f"RESPONSE CODE: {response.status_code}")
            logger.info(f"REASON: {response.reason}")
            logger.info(f'RESPONSE REECEIVED IN {response.elapsed.total_seconds()} SECONDS')
            
            response = response.json()

            return response
            
    except Exception as e:
            logger.error(e)

def create_dataframe(data):
    columninfo = data['reportExtendedMetadata']['detailColumnInfo']
    rows = data['factMap']['T!T']['rows']

    column_headers = [columns for columns in columninfo]

    df = pd.DataFrame(columns=column_headers)
    
    row_data = [row for row in rows]
    
    for i, row in enumerate(row_data):
        values = row["dataCells"]
        labels = [value["label"] for value in values]
        df.loc[i] = labels

    return df
         

query = {
    "query": "Cheddar cheese",
    "dataType": [
        "Foundation",
        "Branded Foods"
    ],
  "pageSize": 25,
  "sortBy": "dataType.keyword",
  "nutrients": [203, 204, 205]
}

if __name__ == "__main__":
    q = search_foods(query)

    with open("result.json", 'w') as f:
        json.dump(q, f, indent=4)

    with open("result.json", 'r') as f:
        data = json.load(f)
        df = pd.DataFrame(columns=["fdcId", "description", "foodCategory", "dataType", "publishedDate"])
        for i, s in enumerate(data['foods']):
            r = [s['fdcId'], s['description'], s['foodCategory'], s['dataType'], s['publishedDate']]
            
            df.loc[i] = r
    
    print(df)
        


    # columninfo = data['reportExtendedMetadata']['detailColumnInfo']
    # rows = data['factMap']['T!T']['rows']

    # column_headers = [columns for columns in columninfo]

    # df = pd.DataFrame(columns=column_headers)
    
    # row_data = [row for row in rows]
    
    # for i, row in enumerate(row_data):
    #     values = row["dataCells"]
    #     labels = [value["label"] for value in values]
    #     df.loc[i] = labels
