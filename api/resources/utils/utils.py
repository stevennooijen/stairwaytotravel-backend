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
