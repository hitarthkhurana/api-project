# RTDS - Real-Time Data Stream

WebSocket streaming for live Polymarket data.

## Comments Stream

Monitor real-time comments across all markets:

```bash
pip install websocket-client
python3 rtds/comments_stream.py
```

**Features:**
- Live comment feed
- User info and pseudonyms
- Event/market associations
- No authentication required

**Example Output:**
```
💬 NEW COMMENT
   User: salted.caramel
   On: Event #18396
   Text: do you know what the term encircle means?...
```

## WebSocket Endpoint

- **URL:** `wss://ws-live-data.polymarket.com`
- **Topics:** `comments`, `crypto_prices`, `crypto_prices_chainlink`
- **Auth:** Not required for public streams

