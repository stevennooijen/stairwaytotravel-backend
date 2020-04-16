def create_one_list_item(df_in, place_id, line_prefix='<li>', line_postfix='.'):
    record = df_in.loc[lambda df: df['id'] == place_id]
    line = line_prefix + record['name'].iloc[0] + ', ' + record['country'].iloc[0] + line_postfix
    return line

def create_list_of_likes(df_in, likes, list_prefix='<ul>', list_postfix='</ul>', **kwargs):
    output = list_prefix
    for like in likes:
        output = output + create_one_list_item(df_in, like, **kwargs)
    output = output + list_postfix
    return output

def prettify_n_results(n):
    thresholds = [300, 1000, 5000, 10000, 20000]
    if n > 300:
        n = '{:,}'.format((max([result for result in thresholds if n > result]))).replace(',', '.') + '+'
    return n
