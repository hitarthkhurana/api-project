# WebSocket Streams

Real-time market data via CLOB WebSocket.

## Market Stream

```bash
python3 websocket/market_stream.py
```

Streams live order book updates and price changes for specific markets.

**Endpoint:** `wss://ws-subscriptions-clob.polymarket.com/ws/market`

## Features

- Real-time order book (bids/asks)
- Price change events
- Last trade price
- Tick size changes

## Usage

Subscribe with asset IDs (token IDs):
```python
{
  "assets_ids": ["token_id_here"],
  "type": "market"
}
```

No authentication required for market data.

