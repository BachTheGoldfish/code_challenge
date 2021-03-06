import csv
import pandas as pd

def create_value(row, df):

    if row['value'] == '':
        index = df.index.get_loc(row.name)
        if index == 0 or index == len(df.index) -1:
           return 1
        else:
           return (df.iloc[index - 1]['value'] + df.iloc[index + 1]['value'])/2
    else:
        return row['value']


def format_date(row):

    if row['date'] == '12/30/1899': # due to Excel's format
        return pd.to_datetime('1899-12-30').strftime('%Y-%m-%d')
    else:
        return pd.to_datetime(row['date']).strftime('%Y-%m-%d')


if __name__ == '__main__':

    file_name = r'C:/Users/Babel/Documents/gridcure_test_data.xlsx'
    output_filename = r'C:/Users/Babel/Documents/gridcure_data_merge.csv'

    data1_df = pd.read_excel(file_name, sheet_name='data1', keep_default_na=False)
    data2_df = pd.read_excel(file_name, sheet_name='data2', keep_default_na=False)
    df1 = pd.merge(data1_df, data2_df,  on='item_id')
    df = pd.DataFrame(columns=['item_id', 'result', 'date', 'new_value'])
    df['item_id'] = df1['item_id']
    df['date'] = df1.apply(lambda row: format_date(row), axis = 1)
    df['result'] = df1.apply(lambda row: (row['mp1']*row['mp2']), axis = 1)
    df['new_value'] = df1.apply(lambda row: create_value(row, df1), axis=1)

    df.to_csv(output_filename, quoting=csv.QUOTE_ALL, index=False, encoding='utf-8', header='column_names')
