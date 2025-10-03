# Polymarket CLI

Python CLI for querying Polymarket prediction markets via REST APIs.

## Quick Start

```bash
pip install -r requirements.txt

python3 polymarket_cli.py search "trump"
python3 polymarket_cli.py event when-will-the-government-shutdown-end
python3 polymarket_cli.py market 0x80dbcce5a1e4e4a1dc
python3 polymarket_cli.py trending
```

## Structure

```
api_client.py      # API wrapper (~40 lines)
polymarket_cli.py  # CLI interface (~200 lines)
API_GUIDE.md       # API documentation
```

## Features

- ✅ **Search** - Find current markets (uses `/public-search`)
- ✅ **Event details** - Get all markets for an event
- ✅ **Market odds** - View prices and implied probabilities  
- ⚠️ **Active markets** - List active markets (not sorted by volume like website)
- No authentication required

## Verified Working

**Search finds LIVE markets:**
```bash
$ python3 polymarket_cli.py search "government shutdown"
✅ Found 4 events
1. 🟢 When will the Government shutdown end?
   Volume: $2,282,650 | Markets: 6
```

**All endpoints tested Oct 3, 2025 - returns current data**

## API Endpoints Used

- `GET /public-search` - Search markets (Gamma)
- `GET /sampling-markets` - Active markets (CLOB)
- `GET /sampling-simplified-markets` - Prices/odds (CLOB)

See [API_GUIDE.md](API_GUIDE.md) for details.

## Tech Stack

Python 3 • requests • Polymarket APIs
