from collections import defaultdict

def get_prs_url(owner: str, name: str):
    return (f'https://api.github.com/repos/{owner}/{name}/pulls')

def find_page_info(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'pageInfo':
                return value
            else:
                result = find_page_info(value)
                if result:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_page_info(item)
            if result:
                return result
    return None

def agroup_results(results):
    grouped_results = defaultdict(lambda: {'time': [], 'size': []})
    
    for result in results:
        key = (result['api'], result['query'])
        grouped_results[key]['time'].append(result['time'])
        grouped_results[key]['size'].append(result['size'])
                
    return grouped_results

def summarize_results(results: list):
    try:
        if len(results) == 0:
            return
        
        data=[]
        summarized_results=agroup_results(results)
                
        for (api, query), metrics in summarized_results.items():
            avg_time = sum(metrics['time']) / len(metrics['time'])
            avg_size = sum(metrics['size']) / len(metrics['size'])
            data.append({'api': api, 'query': query, 'avg_time': avg_time, 'avg_size': avg_size})
                
        return data
        
    except Exception as e:
        print(f"Erro ao sumarizar os resultados: {e}")