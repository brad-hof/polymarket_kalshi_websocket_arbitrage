import requests
import pandas as pd

def get_poly_tag_id(categories):
    base_url = "https://gamma-api.polymarket.com"
    tag_id = []
    for cat in categories:
        tag_response = requests.get(f"{base_url}/tags/slug/{cat.lower()}")
        if tag_response.status_code != 200:
            continue
        tag_data = tag_response.json()
        tag_id_numb = tag_data.get('id')
        tag_id.append(tag_id_numb)
    return tag_id


def fetch_poly_markets (tag_id, date):
    base_url = "https://gamma-api.polymarket.com"
    offset = 0
    limit = 100
    rows = []
    for tag in tag_id:
        url = f"{base_url}/events?tag_id={tag}&closed=false&limit={limit}&offset={offset}&include_tag=true&end_date_max={date}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        for event in data:
            title = event.get('title', '')
            markets = event.get('markets', [])
            for m in markets:
                row = {'event_title': title}
                row.update(m)
                rows.append(row)
        offset += limit
    return rows


def poly_df_and_clobIDs (poly_markets):
    df = pd.DataFrame(poly_markets)
    df = df[df['closed'] != True]
    df = df[df['active'] != False]
    df = df[~df['groupItemTitle'].str.contains('1H', case=False, na=False)]
    df = df[~df['groupItemTitle'].str.contains('Spread', case=False, na=False)]
    df = df[~df['groupItemTitle'].str.contains('O/U', case=False, na=False)]
    df[['outcome_a', 'outcome_b']] = df['outcomes'].str.strip('[]').str.replace('"', '').str.split(', ', expand=True)
    #df = df[df['outcome_a'].str.contains('Brown', case=False, na=False)]
    df[['a', 'b']] = df['clobTokenIds'].str.strip('[]').str.replace('"', '').str.split(', ', expand=True)
    df = df[['event_title', 'outcome_a', 'outcome_b', 'a', 'b']]
    return df


