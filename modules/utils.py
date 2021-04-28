import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from google.cloud import bigquery


def _get_data(task):
    """
      Get a task (DataQuery) and run get_data
      Used for ThreadPoolExecutor
      """
    return task.get_data()

def run_concurrent_queries(list_queries_fetchers):
    """
      Run Queries concruently 
      list_queries_fetchers (List[DataQuery]) is a list of queries fetchers 
      returns dict {DataQuery.name: results}
    """
    max_workers = 5
    results = {}
    print("Starting ThreadPoolExecutor")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(_get_data, (task)): task.name for task in list_queries_fetchers}

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            results[url] = future.result()
  
    print("All tasks complete")
    return results


def estimate_gigabytes_scanned(query, bq_client):
    """
    A useful function to estimate query size. 
    """
    # We initiate a `QueryJobConfig` object
    # API description: https://googleapis.dev/py/bigquery/latest/generated/google.cloud.bigquery.job.QueryJobConfig.html
    my_job_config = bigquery.job.QueryJobConfig()
    
    # We turn on 'dry run', by setting the `QueryJobConfig` object's `dry_run` attribute.
    # This means that we do not actually run the query, but estimate its running cost. 
    my_job_config.dry_run = True

    # We activate the job_config by passing the `QueryJobConfig` to the client's `query` method.
    my_job = bq_client.query(query, job_config=my_job_config)
    
    # The results comes as bytes which we convert into Gigabytes for better readability
    BYTES_PER_GB = 2**30
    estimate = my_job.total_bytes_processed / BYTES_PER_GB
    
    # print(f"This query will process {estimate} GBs.")
    return estimate

