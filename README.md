# Prediction Market Arbitrage Detector (Polymarket - Kalshi)
Find arbitrage opportunities using Kalshi and Polymarket websocket API's.

You will need: Kalshi account & private key

Steps:
1. Update line 12 in `get_poly_clob_tokenID.py` with current date.
1. Run the `get_poly_clob_tokenID.py` script to fetch CLOB tokens for a specific market (Lakers vs Celtics - Lakers) given your category of choice (NBA, MLB, NFL, etc).
2. Update line 15 in the `poly_kalsh_arb_detector.py` script with the CLOB token you just got.
3. Go to the Kalshi website and find the market ticker for the same market but on the other side (Lakers vs Celtics - Celtics).
4. Update line 16 in the `poly_kalsh_arb_detector.py` script with the market ticker you just found.
5. Update line 8 in the `poly_kalsh_arb_detector.py` script with your kalshi key ID and update the `your_kalshi_RSA_private_key.pem` file with your info.
6. Run the `poly_kalsh_arb_detector.py` script in your terminal and watch as it compares live orders between the two websites & finds live price differences.



https://github.com/user-attachments/assets/41e3b361-7ceb-4de2-b639-92ba1272e2b4

