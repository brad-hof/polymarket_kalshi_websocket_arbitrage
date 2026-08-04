# Prediction Market Arbitrage Detector (Polymarket - Kalshi)
Find price arbitrage using the Kalshi and Polymarket websocket API's.

You will need: Kalshi account & private key

Steps:
1. On line 11 in `get_poly_clob_tokenID.py` change to your desired tag_id (mlb is in there as default).
2. Update line 12 in `get_poly_clob_tokenID.py` with the current date.
3. Run the `get_poly_clob_tokenID.py` script to fetch CLOB tokens.
4. For a specific market (Lakers vs Celtics - Lakers) copy and past the CLOB token from one side.
5. Update line 15 in the `poly_kalsh_arb_detector.py` script with the CLOB token you just got.
6. Go to the Kalshi website and find the market ticker for the same market but on the other side (Lakers vs Celtics - Celtics).
7. Update line 16 in the `poly_kalsh_arb_detector.py` script with the market ticker you just found.
8. Update line 8 in the `poly_kalsh_arb_detector.py` script with your kalshi key ID and update the `your_kalshi_RSA_private_key.pem` file with your info.
9. Run the `poly_kalsh_arb_detector.py` script in your terminal and watch as it compares live order ask requests between the two websites.
10. When there's a favorable price difference (the total of both markets <1) the script will print a 'buy' message to the terminal.

See video example below in comparison to their live websites:

https://github.com/user-attachments/assets/41e3b361-7ceb-4de2-b639-92ba1272e2b4

