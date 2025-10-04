# Polymarket Subgraph Tools

Query on-chain Polymarket data via GraphQL subgraphs hosted on Goldsky.

## What are Subgraphs?

Subgraphs index on-chain events from Polygon blockchain:
- **Orders**: Trades, fills, volume stats
- **Positions**: User holdings with PnL tracking
- **Activity**: Splits, merges, redemptions
- **Open Interest**: Total locked value per market

## Quick Start

```bash
# Whale tracker - large trades
python3 whale_tracker.py whales 5000 10

# User positions and PnL
python3 whale_tracker.py user 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb

# Global stats
python3 whale_tracker.py stats

# Market volume
python3 volume_analytics.py volume <token_id>

# Recent on-chain activity
python3 volume_analytics.py splits 20
python3 volume_analytics.py redemptions 15

# Open interest
python3 volume_analytics.py oi
```

## Files

- **`client.py`**: GraphQL client for all 5 subgraphs
- **`whale_tracker.py`**: Monitor large trades and positions
- **`volume_analytics.py`**: Market volume and on-chain activity

## Subgraphs Used

1. **Orderbook** - Trades, fills, volume
2. **PNL** - User positions with avg price & realized profits
3. **Activity** - Splits/merges/redemptions
4. **Open Interest** - Total value locked
5. **Positions** - Holdings data

## Use Cases

- Track whale activity (>$1k trades)
- Monitor user PnL across positions
- Analyze market volume trends
- Watch on-chain conversions (USDC ↔ outcome tokens)
- Calculate total locked value

