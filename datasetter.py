import pandas as pd
import csv
import pag12_submain as p12s

def create_csv(muestra):
    logger.info('Creating dataset...')
    data = []
    for cont in muestra:
        data.append(cont)
    
    df = pd.DataFrame(data)
    return df.to_csv('raw_pagina12_dataset.csv')
    