import os
from google.cloud import bigquery

# Define credentials 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'bigquery-credentials.json'
client = bigquery.Client()

def _fetch_data_bigquery(query):
    """
      Take SQL query in Standard SQL and returns a Pandas DataFrame of results
      ref: https://cloud.google.com/bigquery/docs/reference/standard-sql/enabling-standard-sql
    """
    return client.query(query, location="US").to_dataframe()


class DataQuery:
    """
    Data fetcher
    """
    def __init__(self, name, query, year):
        """
        name: a given name for the query
        query: string standard SQL query
        name: name of the FR name
        year: year
        """
        self.name = name
        self.year = year
        self.query = query % {'name': self.name, 'year': self.year}


    def get_data(self):
        # Repalce name and year in the query
        print('running', self.name, self.year)
        # Get data from BigQuery
        return _fetch_data_bigquery(self.query)