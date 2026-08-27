import duckdb
from datetime import datetime, timedelta

conn = duckdb.connect('restaurant_operations.db')

# Create Raw Telemetry Tables
conn.execute('CREATE OR REPLACE TABLE raw_customer_clicks (event_id VARCHAR, user_id VARCHAR, session_id VARCHAR, platform_channel VARCHAR, target_brand VARCHAR, event_timestamp VARCHAR);')
conn.execute('CREATE OR REPLACE TABLE raw_kitchen_tickets (ticket_id VARCHAR, store_id VARCHAR, brand_name VARCHAR, gross_order_value DOUBLE, ticket_opened VARCHAR, ticket_ready VARCHAR);')
conn.execute('CREATE OR REPLACE TABLE raw_marketplace_commissions (ticket_id VARCHAR, delivery_partner VARCHAR, commission_fee_usd DOUBLE, net_payout_usd DOUBLE);')

# Populate Clickstream User Behavior Data (With null sessions and out-of-order text timestamps)
clicks = [
    ('EV-801', 'USR-401', 'SESS-101', 'Web-App', 'Thistle Greens', '2026-08-06 11:15:00'),
    ('EV-802', 'USR-401', 'SESS-101', 'Web-App', 'Thistle Greens', '2026-08-06 11:17:30'),
    ('EV-803', 'USR-402', None, 'DoorDash-API', 'Burger Craft', '2026-08-06 11:20:10'), # Null Session Anomaly!
    ('EV-804', 'USR-403', 'SESS-102', 'iOS-App', 'Thistle Greens', '2026-08-06 11:02:00')  # Out-of-order delay flag!
]
for click in clicks:
    conn.execute('INSERT INTO raw_customer_clicks VALUES (?, ?, ?, ?, ?, ?)', click)

# Populate Kitchen Telemetry Logs (Capturing prep latencies)
tickets = [
    ('TK-901', 'DEN-01', 'Thistle Greens', 24.50, '2026-08-06 11:18:00', '2026-08-06 11:28:00'),
    ('TK-902', 'DEN-01', 'Burger Craft', 18.00, '2026-08-06 11:22:00', '2026-08-06 11:51:00'), # 29-minute kitchen bottleneck!
    ('TK-903', 'DEN-02', 'Thistle Greens', 32.00, '2026-08-06 11:30:00', '2026-08-06 11:39:00'),
    ('TK-904', 'DEN-01', 'Burger Craft', 15.50, '2026-08-06 12:00:00', None) # Cancelled order anomaly!
]
for tk in tickets:
    conn.execute('INSERT INTO raw_kitchen_tickets VALUES (?, ?, ?, ?, ?, ?)', tk)

# Populate Financial Commissions
commissions = [
    ('TK-901', 'DoorDash', 4.90, 19.60),
    ('TK-902', 'UberEats', 5.40, 12.60),
    ('TK-903', 'DoorDash', 6.40, 25.60)
]
for comm in commissions:
    conn.execute('INSERT INTO raw_marketplace_commissions VALUES (?, ?, ?, ?)', comm)

conn.close()
print('?? Industry-Standard Restaurant FinOps Database Generated!')
