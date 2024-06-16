from collections import defaultdict
import numpy as np
import pandas as pd
from scipy import stats

def get_prs_url(owner: str, name: str):
    return (f'https://api.github.com/repos/{owner}/{name}/pulls')

def find_page_info(data):
    try:
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
    
    except Exception as e:
        print(f"Erro na função find_page_info: {e}")

def agroup_results(results):
    try:
        grouped_results = defaultdict(lambda: {'time': [], 'size': []})
        
        for result in results:
            key = (result['api'], result['query'])
            grouped_results[key]['time'].append(result['time'])
            grouped_results[key]['size'].append(result['size'])
                    
        return grouped_results
    
    except Exception as e:
        print(f"Erro na função agroup_results: {e}")

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
        print(f"Erro na função summarize_results: {e}")
        
def get_column(data: list, *columns: list):
    try:
        df = pd.DataFrame(data)

        if len(columns) == 1:
            return df[columns[0]].tolist()
        else:
            return df[list(columns)].values.tolist()
    
    except Exception as e:
        print(f"Erro na função get_column: {e}")
        
def filter_rows(data: list, column: str, filter: list):
    try:
        df = pd.DataFrame(data)
        return df[df[column].isin(filter)].to_dict('records')
    
    except Exception as e:
        print(f"Erro na função filter_rows: {e}")
        
def student_test(data_1: list, data_2: list, equal_var=True):
    try:
        return stats.ttest_ind(data_1, data_2, equal_var=equal_var)
    
    except Exception as e:
        print(f"Erro na função student_test: {e}")
        
def wilcoxon_test(data_1: list, data_2: list):
    try:
        return stats.wilcoxon(np.array(data_1) - np.array(data_2))
    
    except Exception as e:
        print(f"Erro na função wilcoxon_test: {e}")
        
def normality_test(data: list):
    try:
        _, p_value = stats.shapiro(data)
        return p_value
    
    except Exception as e:
        print(f"Erro na função normality_test: {e}")

def levene_test(data_1: list, data_2: list):
    try:
        return stats.levene(data_1, data_2)
    
    except Exception as e:
        print(f"Erro na função levene_test: {e}")