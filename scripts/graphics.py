from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def bar(bar: str, label: str, data: list, value: str, x_label: str, y_label: str, title: str):
    df = pd.DataFrame(data)
    df_pivot = df.pivot(index=label, columns=bar, values=value)
    
    x = np.arange(len(df_pivot.index))
    width = 0.2
    
    fig, ax = plt.subplots()
    for i, lb in enumerate(df_pivot.columns):
        ax.bar(x + i*width, df_pivot[lb], width, label=lb)
        
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x + width)
    ax.set_xticklabels(df_pivot.index)
    ax.legend()
    
    ax.figure.set_size_inches(10, 6)
    ax.grid(True)
    plt.show()
    
def boxplot(data: list, columns: list, x_label: str, y_label: str, title: str):
    plt.figure(figsize=(6, 4))
    
    plt.boxplot(data, labels=columns)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()