import time
from qr_requests import run_query, run_rest
from queries import GRAPHQL_QUERY
from func_utils import *

OWNER_NAME = 'freeCodeCamp'
REPO_NAME = 'freeCodeCamp'
GRAPHQL_URL = 'https://api.github.com/graphql'
MAX_PULL_REQUESTS = 30
PER_PAGE=10

def measure_graphql():
    start_time = time.time()
        
    has_next_page = True
    cursor = None
    total_response_size = 0
    pull_requests = []
    
    try: 
        while len(pull_requests) <= MAX_PULL_REQUESTS and has_next_page:            
            variables = {
              'owner': OWNER_NAME,
              'name': REPO_NAME,
              'per_page': PER_PAGE,
              'afterCursor': cursor
            }
            
            data, status_code = run_query(GRAPHQL_URL, GRAPHQL_QUERY, variables)
            if not data or 'errors' in data:
                continue
              
            total_response_size += len(data)
            pull_requests.extend(data)
            
            has_next_page = data['data']['repository']['pullRequests']['pageInfo']['hasNextPage']
            cursor = data['data']['repository']['pullRequests']['pageInfo']['endCursor']

    except Exception as e:
        print(f"\nErro durante a execução da consulta (GraphQL): {e}")
    
    finally:
        end_time = time.time()
        response_time = end_time - start_time
        return response_time, total_response_size
    
def measure_rest():
    start_time = time.time()
    
    total_response_size = 0
    pull_requests = []
    page = 1
    
    try:
        while True:
            prs_url = '?state=all&per_page={per_page}&page={page}'.format(per_page=PER_PAGE, page=page)
            prs, status_code = run_rest(get_prs_url(OWNER_NAME, REPO_NAME) + '?state=all&per_page=100&page={page}')
            if not prs or status_code != 200:
                continue
              
            total_response_size += len(prs)
            pull_requests.extend(prs)
            
            if len(pull_requests) <= MAX_PULL_REQUESTS:
                break
            page += 1

        for pr in pull_requests:
            pr_number = pr['number']
            pr_details, status = run_rest(get_prs_url(OWNER_NAME, REPO_NAME) + '/{pr_number}')
            total_response_size += len(pr_details)
            
            pr_reviews, status = run_rest(get_prs_url(OWNER_NAME, REPO_NAME) + '/{pr_number}/reviews')
            total_response_size += len(pr_reviews)
            
            pr_files, status = run_rest(get_prs_url(OWNER_NAME, REPO_NAME) + '/{pr_number}/files')
            total_response_size += len(pr_files)
            
            pr_comments, status = run_rest(get_prs_url(OWNER_NAME, REPO_NAME) + '/{pr_number}/comments')
            total_response_size += len(pr_comments)
        
        
    except Exception as e:
        print(f"\nErro durante a execução da consulta (Rest): {e}")
    
    finally:
        end_time = time.time()
        response_time = end_time - start_time
        return response_time, total_response_size

graphql_times = []
graphql_sizes = []
rest_times = []
rest_sizes = []

print('GraphQL\n')
gql_time, gql_size = measure_graphql()
graphql_times.append(gql_time)
graphql_sizes.append(gql_size)

print('Rest\n')
rest_time, rest_size = measure_rest()
rest_times.append(rest_time)
rest_sizes.append(rest_size)

def analyze_results(times, sizes, method):
    avg_time = sum(times) / len(times)
    avg_size = sum(sizes) / len(sizes)
    print(f'{method} - Average Time: {avg_time:.4f} seconds')
    print(f'{method} - Average Size: {avg_size} bytes')

print('GraphQL Results:')
analyze_results(graphql_times, graphql_sizes, 'GraphQL')

print('REST Results:')
analyze_results(rest_times, rest_sizes, 'REST')
