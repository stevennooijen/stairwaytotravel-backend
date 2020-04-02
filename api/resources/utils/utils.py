def create_one_html_list_item(df_in, place_id):
    record = df_in.loc[lambda df: df['id'] == place_id]
    html = '<li>' + record['name'].iloc[0] + ', ' + record['country'].iloc[0] + '.'
    return html

def create_html_list_of_likes(df_in, likes):
    html = '<ul>'
    for like in likes:
        html = html + create_one_html_list_item(df_in, like)
    html = html + '</ul>'
    return html
