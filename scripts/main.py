import time
from qr_requests import run_query, run_rest
from queries import COMPLEX_QUERY, SIMPLE_QUERY
from func_utils import *
from save_data import save_to_csv

RUN_TIMES=10
MAX_REPOS=100
MAX_PULL_REQUESTS=100
PER_PAGE=10
OWNER_NAME='freeCodeCamp'
REPO_NAME='freeCodeCamp'

def measure_graphql(limit: int, query: str, owner: str=None, repo: str=None):
    start_time=time.time()
        
    has_next_page=True
    cursor=None
    total_response_size=0
    GRAPHQL_URL='https://api.github.com/graphql'
    
    try: 
        for _ in range(limit // PER_PAGE):
            if not has_next_page:
                break
                    
            variables={
              'per_page': PER_PAGE,
              'cursor': cursor
            }
            
            if owner and repo:
                variables['owner']=owner
                variables['name']=repo
            
            response=run_query(GRAPHQL_URL, query, variables)
            
            if not response:
                continue
              
            total_response_size += len(response.content)
            data=response.json()
                    
            page_info = find_page_info(data['data'])
            has_next_page = page_info['hasNextPage']
            cursor = page_info['endCursor']

    except Exception as e:
        print(f"\nErro durante a execução da consulta (GraphQL): {e}")
    
    finally:
        end_time=time.time()
        response_time=end_time - start_time
        return response_time, total_response_size
    

def measure_rest_simple_query(limit):
    start_time = time.time()

    total_response_size = 0
    repos = []
    page = 1
    
    BASE_URL = "https://api.github.com"
    SEARCH_REPOS_URL = f"{BASE_URL}/search/repositories"

    try:
        while len(repos) < (limit // PER_PAGE):
            response = run_rest(f"{SEARCH_REPOS_URL}?q=stars:>0&sort=stars&order=desc&per_page={PER_PAGE}&page={page}")
            
            if not response:
                continue
            
            total_response_size += len(response.content)
            repos.extend(response.json().get('items', []))
                        
            page += 1
        
        for repo in repos:
            repo_name_with_owner = repo['full_name']
            
            pr_response = run_rest(f"{BASE_URL}/repos/{repo_name_with_owner}/pulls?state=all")
            if pr_response:
                total_response_size += len(pr_response.content)

    except Exception as e:
        print(f"\nErro durante a execução da consulta (REST): {e}")

    finally:
        end_time = time.time()
        response_time = end_time - start_time
        return response_time, total_response_size

def measure_rest_complex_query(limit):
    start_time=time.time()

    total_response_size=0
    prs=[]
    page=1

    try:
        while(len(prs) < (limit // PER_PAGE)):
            response=run_rest(get_prs_url(OWNER_NAME, REPO_NAME) + f'?state=all&per_page={PER_PAGE}&page={page}')
            
            if not response:
                continue
            
            total_response_size += len(response.content)
            prs.extend(response.json())
        
            page += 1

        for pr in prs:
            number=pr['number']
            
            pr_details=run_rest(get_prs_url(OWNER_NAME, REPO_NAME) + f'/{number}')
            if pr_details:
                total_response_size += len(pr_details.content)
        
            pr_reviews=run_rest(get_prs_url(OWNER_NAME, REPO_NAME) + f'/{number}/reviews')
            if pr_reviews:
                total_response_size += len(pr_reviews.content)
        
            pr_files=run_rest(get_prs_url(OWNER_NAME, REPO_NAME) + f'/{number}/files')
            if pr_files:
                total_response_size += len(pr_files.content)
        
            pr_comments=run_rest(get_prs_url(OWNER_NAME, REPO_NAME) + f'/{number}/comments')
            if pr_comments:
                total_response_size += len(pr_comments.content)
    
    
    except Exception as e:
        print(f"\nErro durante a execução da consulta (Rest): {e}")

    finally:
        end_time=time.time()
        response_time=end_time - start_time
        return response_time, total_response_size
    


def main():
    results=[]
    summarized_results=[]
    
    print('GraphQL - Simple query\n')
    graphql_times=[]
    graphql_sizes=[]
    limit = MAX_REPOS

    for _ in range(RUN_TIMES):
        gql_time, gql_size=measure_graphql(limit, SIMPLE_QUERY)
        graphql_times.append(gql_time)
        graphql_sizes.append(gql_size)
    
        results.append({'api': 'GraphQL', 'query': 'Simple', 'time': gql_time, 'size': gql_size})

    print('GraphQL - Complex query\n')
    graphql_times.clear()
    graphql_sizes.clear()
    limit = MAX_PULL_REQUESTS
    
    for _ in range(RUN_TIMES):
        gql_time, gql_size=measure_graphql(limit, COMPLEX_QUERY, OWNER_NAME, REPO_NAME)
        graphql_times.append(gql_time)
        graphql_sizes.append(gql_size)
    
        results.append({'api': 'GraphQL', 'query': 'Complex', 'time': gql_time, 'size': gql_size})

    save_to_csv(results, 'gql_results.csv')
    summarized_results=results.copy()
    results.clear()
    
    print('Rest - Simple query\n')
    rest_times=[]
    rest_sizes=[]
    limit = MAX_REPOS

    for _ in range(RUN_TIMES):
        rest_time, rest_size=measure_rest_simple_query(limit)
        rest_times.append(rest_time)
        rest_sizes.append(rest_size)
        
        results.append({'api': 'Rest', 'query': 'Simple', 'time': rest_time, 'size': rest_size})
        
    print('Rest - Complex query\n')
    rest_times.clear()
    rest_sizes.clear()
    limit = MAX_PULL_REQUESTS
    
    for _ in range(RUN_TIMES):
        rest_time, rest_size=measure_rest_complex_query(limit)
        rest_times.append(rest_time)
        rest_sizes.append(rest_size)
        
        results.append({'api': 'Rest', 'query': 'Complex', 'time': rest_time, 'size': rest_size})
        
    save_to_csv(results, 'rest_results.csv')
    summarized_results.extend(results)
        
    data=summarize_results(summarized_results)
    save_to_csv(data, 'avg_results.csv')
        

main()