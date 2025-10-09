"""
Hot Markets - Find markets with sudden trading activity
"""
import requests
from datetime import datetime

ORDERS_SUBGRAPH = "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/orderbook-subgraph/0.0.1/gn"

query = """
{
  orderFilledEvents(first: 100, orderBy: timestamp, orderDirection: desc) {
    timestamp
    makerAssetId
    takerAmountFilled
  }
}
"""

response = requests.post(ORDERS_SUBGRAPH, json={"query": query}, timeout=10)
trades = response.json()["data"]["orderFilledEvents"]

latest_trade_time = datetime.fromtimestamp(int(trades[0]["timestamp"]))
print(f"\n🔥 HOT MARKETS (Last 100 Trades)")
print(f"Latest trade: {latest_trade_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

volume_by_market = {}
for trade in trades:
    market_id = trade["makerAssetId"][:20]
    volume = int(trade["takerAmountFilled"]) / 10**6
    volume_by_market[market_id] = volume_by_market.get(market_id, 0) + volume

hot_markets = sorted(volume_by_market.items(), key=lambda x: x[1], reverse=True)[:10]

for i, (market_id, volume) in enumerate(hot_markets, 1):
    print(f"{i}. {market_id}... → ${volume:,.0f}")
