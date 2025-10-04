# Market Analytics

Advanced market analysis tools for liquidity, slippage, and trading activity.

## Tools

### Liquidity Analyzer
Analyze order book depth and calculate slippage for different trade sizes.

```bash
# View order book depth
python3 liquidity_analyzer.py depth <token_id> 10

# Calculate slippage for a trade
python3 liquidity_analyzer.py slippage <token_id> 100 BUY
```

**Features:**
- Order book depth visualization (bids/asks)
- Bid-ask spread calculation
- Slippage estimation for any trade size
- Total liquidity metrics

### Top Markets
Find most active markets by volume or trade count.

```bash
# Top markets by volume
python3 top_markets.py volume 20

# Most traded markets
python3 top_markets.py trades 15
```

**Metrics:**
- Total volume
- Trade count
- Buy/Sell ratio
- Average trade size

## Use Cases

- **Pre-trade analysis**: Check liquidity before placing large orders
- **Slippage estimation**: Know your execution price before trading
- **Market discovery**: Find most active/liquid markets
- **Spread analysis**: Identify tight vs wide spread markets

