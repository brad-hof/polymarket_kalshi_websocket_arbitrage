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


def fetch_poly_markets(tag_id, target_date):
    """
    target_date: plain 'YYYY-MM-DD' string for the game date you want (e.g. '2026-07-29')
    """
    base_url = "https://gamma-api.polymarket.com"
    limit = 100
    rows = []

    for tag in tag_id:
        offset = 0
        while True:
            url = (
                f"{base_url}/events?tag_id={tag}&closed=false&limit={limit}"
                f"&offset={offset}&include_tag=true"
                f"&order=startDate&ascending=false"
            )
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            for event in data:
                title = event.get('title', '')
                event_date = event.get('eventDate')
                markets = event.get('markets', [])
                for m in markets:
                    row = {'event_title': title, 'event_date': event_date}
                    row.update(m)
                    rows.append(row)
            offset += limit
            if len(data) < limit:
                break

    rows = [r for r in rows if r.get('event_date') == target_date]
    return rows


def poly_df_and_clobIDs(poly_markets):
    df = pd.DataFrame(poly_markets)
    df = df[df['closed'] != True]
    df = df[df['active'] != False]
    df = df[df['sportsMarketType'] == 'moneyline']
    df[['outcome_a', 'outcome_b']] = df['outcomes'].str.strip('[]').str.replace('"', '').str.split(', ', expand=True)
    df[['a', 'b']] = df['clobTokenIds'].str.strip('[]').str.replace('"', '').str.split(', ', expand=True)
    df = df[['event_title', 'event_date', 'outcome_a', 'outcome_b', 'a', 'b']]
    return df

