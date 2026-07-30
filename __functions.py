import time
import base64
import requests
import pandas as pd
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def get_poly_tag_id(categories: list[str]) -> list[str]:
    """
    Look up the Polymarket tag id for each category slug.
    """
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


def fetch_poly_markets(tag_id: list[str], target_date: str) -> list[dict[str]]:
    """
    Fetch markets for the given tags, filtered to one game date ('YYYY-MM-DD').
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


def poly_df_and_clobIDs(poly_markets: list[dict[str]]) -> pd.DataFrame:
    """
    Build a dataframe of moneyline markets with outcome names and CLOB token ids.
    """
    df = pd.DataFrame(poly_markets)
    df = df[df['closed'] != True]
    df = df[df['active'] != False]
    df = df[df['sportsMarketType'] == 'moneyline']
    df[['outcome_a', 'outcome_b']] = df['outcomes'].str.strip('[]').str.replace('"', '').str.split(', ', expand=True)
    df[['a', 'b']] = df['clobTokenIds'].str.strip('[]').str.replace('"', '').str.split(', ', expand=True)
    df = df[['event_title', 'event_date', 'outcome_a', 'outcome_b', 'a', 'b']]
    return df


def kalsh_header_for_wss(key_id):
    KEY_ID = key_id
    with open("path/to/your/Kalshi/RSAPrivateKey.pem", "r") as f:
        PRIVATE_KEY_PEM = f.read()
    private_key = serialization.load_pem_private_key(PRIVATE_KEY_PEM.encode('utf-8'), password=None)
    timestamp = str(int(time.time() * 1000))
    message = timestamp + "GET" + "/trade-api/ws/v2"
    signature = private_key.sign(
                    message.encode('utf-8'),
                    padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.DIGEST_LENGTH),  # FIX: was MAX_LENGTH
                    hashes.SHA256())
    sig_b64 = base64.b64encode(signature).decode('utf-8')
    headers = {
        "KALSHI-ACCESS-KEY": KEY_ID,
        "KALSHI-ACCESS-SIGNATURE": sig_b64,
        "KALSHI-ACCESS-TIMESTAMP": timestamp,
    }
    return headers

