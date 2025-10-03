# Polymarket API Explorer

Python tools for Polymarket prediction markets - REST APIs and WebSocket streams.

## Quick Start

```bash
pip install -r requirements.txt

# REST API
python3 polymarket_cli.py search "trump"
python3 polymarket_cli.py market 0x80dbcce5a1e4e4a1dc

# WebSocket Streams
python3 websocket/live_tracker.py       # Real-time market data
python3 rtds/comments_stream.py         # Real-time comments
```

## Project Structure

```
api_client.py              # REST API wrapper
polymarket_cli.py          # CLI tool
websocket/
  ├── live_tracker.py      # Enhanced market stream with analytics
  └── market_stream.py     # Basic market websocket
rtds/
  └── comments_stream.py   # Real-time comments feed
API_GUIDE.md               # Complete API documentation
```

## Features

**REST API:**
- ✅ Search current markets (`/public-search`)
- ✅ Event details with all markets
- ✅ Market odds and implied probabilities
- ✅ Active markets listing

**WebSocket Streams:**
- ✅ Real-time order book updates
- ✅ Bid-ask spread analytics
- ✅ Live price changes
- ✅ Trade execution monitoring
- ✅ Real-time comments feed

No authentication required for public data.

## Verified Working

**Search finds LIVE markets:**
```bash
$ python3 polymarket_cli.py search "government shutdown"
✅ Found 4 events
1. 🟢 When will the Government shutdown end?
   Volume: $2,282,650 | Markets: 6
```

## Endpoints Used

**REST:**
- `GET /public-search` - Search markets
- `GET /sampling-simplified-markets` - Live prices/odds
- `GET /sampling-markets` - Active markets

**WebSocket:**
- `wss://ws-subscriptions-clob.polymarket.com/ws/market` - Order book
- `wss://ws-live-data.polymarket.com` - Comments & crypto prices

See [API_GUIDE.md](API_GUIDE.md) for complete documentation.

## Tech Stack

Python 3 • requests • websocket-client • Polymarket APIs
