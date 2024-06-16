import os
import pandas as pd

ROOT_PATH = os.getcwd().replace('\\', '/')
SAVE_PATH = ROOT_PATH + '/scripts/dataset/'


def save_to_csv(results: list, filename: str):
    try:
        if len(results) == 0:
            return
        
        df = pd.DataFrame(results)
        df.to_csv(SAVE_PATH + filename, index=False)

    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        
def read_csv(filename: str):
    try:
        return pd.read_csv(SAVE_PATH + filename).to_dict('records')
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado")