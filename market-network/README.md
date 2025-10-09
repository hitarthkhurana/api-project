# Market Correlation Network

**See which prediction markets share common traders.**

Interactive force-directed graph showing connections between Polymarket prediction markets based on trader overlap. Markets are nodes, connections show shared traders (Jaccard similarity >5%).

## Concept

Traders active in multiple markets reveal hidden correlations. If many traders bet on both "Fed Rate Decision" and "Inflation Target", these markets are related in ways beyond categories.

This tool helps identify:
- Cross-market trading patterns
- Trader behavior clusters
- Hidden market relationships
- Category correlations

## Tech Stack

- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, shadcn/ui
- **Visualization:** D3.js force-directed graph
- **Data Source:** Static JSON (pre-fetched from APIs)
- **APIs Used:**
  - Gamma API → Market metadata (questions, categories, volume)
  - PNL Subgraph → Trader positions (on-chain data)

## Data Pipeline

```bash
# Fetch data (Python)
cd scripts
python3 fetch_data.py

# Generates public/network.json with:
# - nodes: markets (question, category, volume, trader count)
# - edges: connections (overlap percentage)
```

**Default:** 189 markets, 3094 connections, $583M volume

## How It Works

1. **Fetch Markets:** Gamma API `/events` endpoint (sorted by 24h volume)
2. **Get Traders:** PNL Subgraph queries `userPositions` for each market token
3. **Calculate Overlap:** Jaccard similarity = |A ∩ B| / |A ∪ B|
4. **Filter:** Only show connections >5% overlap
5. **Visualize:** D3 force simulation with category colors

## APIs & Data

**Gamma API** (REST):
- `GET /events?closed=false&limit=10&order=volume24hr`
- Returns market questions, categories, volume, token IDs

**PNL Subgraph** (GraphQL):
```graphql
query {
  userPositions(where: {tokenId: "..."}) {
    user
  }
}
```
- Returns all traders holding a specific market token
- Hosted on Goldsky (public endpoint)

**Why Subgraphs?**  
Trader positions are on-chain data. No REST endpoint exists for "who holds token X". PNL Subgraph indexes blockchain events in real-time.

## Project Structure

```
market-network/
├── scripts/
│   └── fetch_data.py      # Data fetching script (Python)
├── public/
│   └── network.json       # Static network data
└── README.md
```

## Run Locally

```bash
# Generate fresh data
cd scripts
pip install requests
python3 fetch_data.py

# Edit limit in fetch_data.py:
# get_active_markets(10)  → 10 events (~200 markets)
# get_active_markets(50)  → 50 events (~800 markets)
```

## Notes

- **Static Data:** Pre-fetched for demo stability (no API failures)
- **Read-Only:** No authentication required
- **Open Source:** All code available, uses public Polymarket APIs
- **Legal:** Read-only data access is unrestricted

Built to explore Polymarket's API ecosystem and demonstrate data visualization.


