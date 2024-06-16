import time
from qr_requests import run_query, run_rest
from queries import COMPLEX_QUERY, SIMPLE_QUERY
from func_utils import *
from save_data import *
from graphics import *

RUN_TIMES=10
MAX_REPOS=100
MAX_PULL_REQUESTS=100
PER_PAGE=10
OWNER_NAME='freeCodeCamp'
REPO_NAME='freeCodeCamp'
ALPHA=0.05

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
        while (len(repos) < (limit // PER_PAGE)):
            response = run_rest(f"{SEARCH_REPOS_URL}?q=stars:>1&sort=stars&order=desc&per_page={PER_PAGE}&page={page}")
            
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
        print(f"\nErro durante a execução da consulta (REST): {e}")

    finally:
        end_time=time.time()
        response_time=end_time - start_time
        return response_time, total_response_size
    
def main():
    summarized_results=[]
    
    print('GraphQL - Simple query\n')
    graphql_times=[]
    graphql_sizes=[]
    gql_results=[]
    limit = MAX_REPOS

    for _ in range(RUN_TIMES):
        gql_time, gql_size=measure_graphql(limit, SIMPLE_QUERY)
        graphql_times.append(gql_time)
        graphql_sizes.append(gql_size)
    
        gql_results.append({'api': 'GraphQL', 'query': 'Simple', 'time': gql_time, 'size': gql_size})

    print('GraphQL - Complex query\n')
    graphql_times.clear()
    graphql_sizes.clear()
    limit = MAX_PULL_REQUESTS
    
    for _ in range(RUN_TIMES):
        gql_time, gql_size=measure_graphql(limit, COMPLEX_QUERY, OWNER_NAME, REPO_NAME)
        graphql_times.append(gql_time)
        graphql_sizes.append(gql_size)
    
        gql_results.append({'api': 'GraphQL', 'query': 'Complex', 'time': gql_time, 'size': gql_size})

    save_to_csv(gql_results, 'gql_results.csv')
    summarized_results.extend(gql_results)
    
    print('REST - Simple query\n')
    rest_times=[]
    rest_sizes=[]
    rest_results=[]
    limit = MAX_REPOS

    for _ in range(RUN_TIMES):
        rest_time, rest_size=measure_rest_simple_query(limit)
        rest_times.append(rest_time)
        rest_sizes.append(rest_size)
        
        rest_results.append({'api': 'REST', 'query': 'Simple', 'time': rest_time, 'size': rest_size})
        
    print('REST - Complex query\n')
    rest_times.clear()
    rest_sizes.clear()
    limit = MAX_PULL_REQUESTS
    
    for _ in range(RUN_TIMES):
        rest_time, rest_size=measure_rest_complex_query(limit)
        rest_times.append(rest_time)
        rest_sizes.append(rest_size)
        
        rest_results.append({'api': 'REST', 'query': 'Complex', 'time': rest_time, 'size': rest_size})
        
    save_to_csv(rest_results, 'rest_results.csv')
    summarized_results.extend(rest_results)
        
    avg_results=summarize_results(summarized_results)
    save_to_csv(avg_results, 'avg_results.csv')
    
    # avg_results = read_csv('avg_results.csv')
        
    # Gráficos de Barras
    bar(
        data=avg_results,
        bar='query',
        label='api',
        value='avg_time',
        x_label='Tipo de Query',
        y_label='Tempo Médio (s)',
        title='Gráfico de Barras do Tempo Médio por API e Tipo de Query'
    )
    bar(
        data=avg_results,
        bar='query',
        label='api',
        value='avg_size',
        x_label='Tipo de Query',
        y_label='Tamanho Médio (bytes)',
        title='Gráfico de Barras do Tamanho Médio por API e Tipo de Query'
    )
    
    # gql_results = read_csv('gql_results.csv')
    # rest_results = read_csv('rest_results.csv')
    
    # Boxplots
    simple_gql_time_results = get_column(filter_rows(gql_results, 'query', ['Simple']), 'time')  
    boxplot(
        data=simple_gql_time_results,
        columns=['GraphQL'],
        x_label='Query Simples',
        y_label='Tempo (segundos)',
        title='Boxplot do Tempo (segundos) por API e Query Simples'
    )
    
    complex_gql_time_results = get_column(filter_rows(gql_results, 'query', ['Complex']), 'time')
    boxplot(
        data=complex_gql_time_results,
        columns=['GraphQL'],
        x_label='Query Complexa',
        y_label='Tempo (segundos)',
        title='Boxplot do Tempo (segundos) por API e Query Complexa'
    )
    
    simple_rest_time_results = get_column(filter_rows(rest_results, 'query', ['Simple']), 'time')
    boxplot(
        data=simple_rest_time_results,
        columns=['REST'],
        x_label='Query Simples',
        y_label='Tempo (segundos)',
        title='Boxplot do Tempo (segundos) por API e Query Simples'
    )
    
    complex_rest_time_results = get_column(filter_rows(rest_results, 'query', ['Complex']), 'time')
    boxplot(
        data=complex_rest_time_results,
        columns=['REST'],
        x_label='Query Complexa',
        y_label='Tempo (segundos)',
        title='Boxplot do Tempo (segundos) por API e Query Complexa'
    )
    
    # Test t
    graphql_simple = filter_rows(gql_results, 'query', ['Simple'])
    graphql_complex = filter_rows(gql_results, 'query', ['Complex'])
    rest_simple = filter_rows(rest_results, 'query', ['Simple'])
    rest_complex = filter_rows(rest_results, 'query', ['Complex'])
    
    # RQ1 - Tempo de Resposta
    print('\nRQ1 - Teste de Hipótese para Tempo de Resposta')
        
    gql_time = get_column(graphql_simple, 'time')
    rest_time = get_column(rest_simple, 'time')
    
    t_simple, p_simple = student_test(gql_time, rest_time)
    print(f"Teste Consulta Simples: t-statistic= {t_simple}, p-value= {p_simple}")
    
    gql_time = get_column(graphql_complex, 'time')
    rest_time = get_column(rest_complex, 'time')
    
    t_complex, p_complex = student_test(gql_time, rest_time)
    print(f"Teste Consulta Complexa: t-statistic= {t_complex}, p-value= {p_complex}")
    
    # RQ2 - Tamanho da Resposta
    print('\nRQ2 - Teste de Hipótese para Tamanho da Resposta')
    
    gql_sizes = get_column(graphql_simple, 'size')
    rest_sizes = get_column(rest_simple, 'size')
    
    _, p_value = wilcoxon_test(gql_sizes, rest_sizes)
    print(f"Teste Consulta Simples: p-value= {p_value}")
    
    gql_sizes = get_column(graphql_complex, 'size')
    rest_sizes = get_column(rest_complex, 'size')
    
    _, p_value = wilcoxon_test(gql_sizes, rest_sizes)
    print(f"Teste Consulta Complexa: p-value= {p_value}")
        

if __name__ == '__main__':
    main()