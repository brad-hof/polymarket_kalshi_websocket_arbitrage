import pandas as pd
from __functions import get_poly_tag_id
from __functions import fetch_poly_markets
from __functions import poly_df_and_clobIDs

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


clobbbbb = get_poly_tag_id(['mlb'])
clobbbbb

rows = fetch_poly_markets(clobbbbb, '2026-07-28T07:00:00Z')
rows

final = poly_df_and_clobIDs(rows)
final

