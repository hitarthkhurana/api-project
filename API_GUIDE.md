# Polymarket API Reference

## Endpoints Overview

| API | Endpoint | Purpose |
|-----|----------|---------|
| Gamma | `/public-search` | Search markets/events |
| CLOB | `/sampling-markets` | Active markets |
| CLOB | `/sampling-simplified-markets` | Prices/odds |

## 1. Gamma API

**Base:** `https://gamma-api.polymarket.com`

### Public Search
```
GET /public-search?q=<query>&limit_per_type=20&events_status=active
```

Returns current events and markets. Best endpoint for up-to-date data.

### Other Endpoints
- `/markets` - Market list (cached)
- `/events` - Event list (cached)
- `/tags` - Categories

## 2. CLOB API

**Base:** `https://clob.polymarket.com`

### Sampling Markets
```
GET /sampling-markets
```

Returns active markets with metadata.

### Simplified Markets
```
GET /sampling-simplified-markets
```

Returns current prices and token IDs.

### Markets
```
GET /markets
```

Full market list (500 item cache).

## 3. Subgraph (GraphQL)

**Base:** `https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/...`

### What is Subgraph?

Indexes **on-chain events** from Polygon blockchain. Polymarket is hybrid:
- **Off-chain:** Order matching (CLOB - fast, no gas)
- **On-chain:** Settlement, token moves (Polygon - recorded forever)

### What's on blockchain:
- ✅ Trade settlements (when orders execute)
- ✅ Token splits/merges
- ✅ Redemptions (claiming winnings)
- ❌ Order book (off-chain)
- ❌ Unmatched orders (off-chain)

### Use Cases:
- Whale tracking (large on-chain moves)
- Historical volume analysis
- Wallet position tracking
- Settlement patterns

### Available Subgraphs:
- **Activity:** Splits, merges, redemptions
- **Positions:** User token balances
- **Orders:** Order fills (on-chain settlements)
- **PnL:** Profit/loss tracking

### Example Query:
```graphql
{
  splits(first: 10, orderBy: timestamp, orderDirection: desc) {
    id
    timestamp
    amount
    stakeholder
  }
}
```

Test with curl:
```bash
curl -X POST https://api.goldsky.com/.../activity-subgraph/0.0.4/gn \
  -H "Content-Type: application/json" \
  -d '{"query":"{ splits(first: 3) { id timestamp } }"}'
```

## 4. WebSocket RTDS

**Base:** `wss://ws-live-data.polymarket.com`

Real-time streams for prices and comments.

## Rate Limits

- Gamma: 750 req/10s
- CLOB: 5000 req/10s

## Architecture Notes

**Hybrid System:**
- Off-chain: Order matching (CLOB)
- On-chain: Settlement (Polygon)

**Data Sources:**
- CLOB API → Live prices, order book
- Gamma API → Market metadata
- Subgraph → Blockchain events
