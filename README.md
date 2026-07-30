# Prediction Market Arbitrage Detector (Polymarket - Kalshi)
Find arbitrage opportunities using Kalshi and Polymarket websocket API's.

1. Use the `get_poly_clob_tokenID.py` script to fetch the CLOB token for a specific market (Lakers vs Celtics - Lakers) given your category of choice (NBA, MLB, NFL, etc).
2. Go to the Kalshi website and find the market ticker for the same market but on the other side (Lakers vs Celtics - Celtics).
3. Plug in both the poly CLOB token and then Kalshi market ticker where it says in `poly_kalsh_arb_detector.py` script.
4. Run the `poly_kalsh_arb_detector.py` script in your terminal and watch as it compares live orders between the two websites and looks for discrepancies.

