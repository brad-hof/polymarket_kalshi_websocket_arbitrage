import pandas as pd
from __functions import get_poly_tag_id
from __functions import fetch_poly_markets
from __functions import poly_df_and_clobIDs

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

if __name__ == "__main__":
    tag_id = get_poly_tag_id(['mlb'])
    rows = fetch_poly_markets(tag_id, '2026-07-29')
    final_df = poly_df_and_clobIDs(rows)
    print(final_df)

