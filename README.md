# Polymarket Projects

Two projects exploring Polymarket's APIs and prediction markets.

## 📊 Event Network (market-network/)

**Interactive visualization showing which prediction markets share common traders.**

Uses force-directed graph (D3.js) to reveal market correlations based on trader overlap. Helps identify cross-market patterns and trader behavior.

**Tech:** Next.js, TypeScript, Tailwind CSS, D3.js  
**APIs:** Gamma (market data), PNL Subgraph (trader positions)

[See market-network/README.md](market-network/README.md)

---

## 🔧 API Testing Tools (api-testing/)

Python CLI tools and scripts for Polymarket API exploration:

- **REST APIs:** Search markets, get odds, active markets
- **WebSocket:** Real-time market data and comments
- **Subgraph:** Whale tracking, volume analytics, top holders
- **Analytics:** Liquidity depth, slippage, top markets

**Quick Start:**
```bash
cd api-testing
pip install -r requirements.txt

# Search markets
python3 polymarket_cli.py search "election"

# Real-time data
python3 websocket/live_tracker.py

# Analytics
python3 analytics/top_markets.py volume 10
```

[See api-testing/ for full documentation](api-testing/)

---

## Project Structure

```
api-project/
├── market-network/       # Frontend visualization project
│   ├── scripts/          # Data fetching (Python)
│   └── public/           # Static data & frontend
│
└── api-testing/          # API exploration tools
    ├── polymarket_cli.py # Main CLI
    ├── websocket/        # Real-time streams
    ├── subgraph/         # On-chain data queries
    └── analytics/        # Market analysis tools
```

## Tech Stack

**Frontend:** Next.js, TypeScript, Tailwind CSS, shadcn/ui, D3.js  
**Backend/Scripts:** Python 3, requests, websocket-client  
**APIs:** Gamma (REST), CLOB (REST), Subgraphs (GraphQL), WebSocket

No authentication required for read-only endpoints.
