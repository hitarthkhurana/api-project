# WebSocket Streams

Real-time market data via CLOB WebSocket.

## Live Market Tracker (Enhanced)

```bash
python3 websocket/live_tracker.py
```

**Features:**
- Real-time order book tracking
- Bid-ask spread calculation
- Mid-price analytics
- Trade execution monitoring
- Multi-market support
- Price history tracking

## Basic Market Stream

```bash
python3 websocket/market_stream.py
```

Simple stream of order book updates and price changes.

## Endpoint

`wss://ws-subscriptions-clob.polymarket.com/ws/market`

## Example Output

```
[23:45:12] 📊 ORDER BOOK - 713210456792522...
   Best Bid: $0.520 (150 shares)
   Best Ask: $0.530 (200 shares)
   Spread: $0.0100 (1.89%)
   Mid Price: $0.525

[23:45:15] 🔥 TRADE EXECUTED - 713210456792522...
   Side: BUY | Price: $0.530 | Size: 50.00
```

No authentication required for market data.

