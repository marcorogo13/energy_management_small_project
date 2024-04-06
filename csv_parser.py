import pandas as pd

def parse_csv(input_file):
    data = pd.read_csv(input_file, header=0, sep=',')
    print ("Data Columns: ", data.columns)
    return data

