"""
Volume Analytics - Track market volume and on-chain activity
"""
import sys
from datetime import datetime
from client import SubgraphClient

def format_usdc(amount_str: str) -> str:
    """Convert USDC amount to readable format"""
    try:
        amount = int(amount_str) / 10**6
        return f"${amount:,.2f}"
    except:
        return amount_str

def format_timestamp(ts_str: str) -> str:
    """Convert Unix timestamp to readable date"""
    try:
        ts = int(ts_str)
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ts_str

def market_volume(token_id: str):
    """Get volume stats for a specific market"""
    print(f"\n📈 MARKET VOLUME - Token: {token_id}\n")
    
    client = SubgraphClient()
    result = client.get_market_volume(token_id)
    
    if not result or "orderbook" not in result or not result["orderbook"]:
        print("Market not found or no trading data")
        return
    
    book = result["orderbook"]
    
    trades = int(book["tradesQuantity"])
    buys = int(book["buysQuantity"])
    sells = int(book["sellsQuantity"])
    volume = float(book["scaledCollateralVolume"])
    buy_vol = float(book["scaledCollateralBuyVolume"])
    sell_vol = float(book["scaledCollateralSellVolume"])
    
    print(f"Total Trades: {trades:,}")
    print(f"  Buys: {buys:,} ({buys/trades*100:.1f}%)")
    print(f"  Sells: {sells:,} ({sells/trades*100:.1f}%)")
    print(f"\nTotal Volume: ${volume:,.2f}")
    print(f"  Buy Volume: ${buy_vol:,.2f}")
    print(f"  Sell Volume: ${sell_vol:,.2f}")
    
    if trades > 0:
        avg_trade = volume / trades
        print(f"\nAverage Trade Size: ${avg_trade:,.2f}")

def recent_splits(limit: int = 10):
    """Show recent USDC → outcome token conversions"""
    print(f"\n💸 RECENT SPLITS (USDC → Outcome Tokens)\n")
    
    client = SubgraphClient()
    result = client.get_recent_splits(limit=limit)
    
    if not result or "splits" not in result:
        print("No splits found")
        return
    
    splits = result["splits"]
    
    for split in splits:
        amount = format_usdc(split["amount"])
        timestamp = format_timestamp(split["timestamp"])
        stakeholder = split["stakeholder"][:10] + "..."
        
        print(f"{timestamp} | {stakeholder} | {amount}")
        print(f"  Condition: {split['condition'][:20]}...")
        print()

def recent_redemptions(limit: int = 10):
    """Show recent outcome token → USDC redemptions"""
    print(f"\n💰 RECENT REDEMPTIONS (Outcome Tokens → USDC)\n")
    
    client = SubgraphClient()
    result = client.get_recent_redemptions(limit=limit)
    
    if not result or "redemptions" not in result:
        print("No redemptions found")
        return
    
    redemptions = result["redemptions"]
    
    for redemp in redemptions:
        payout = format_usdc(redemp["payout"])
        timestamp = format_timestamp(redemp["timestamp"])
        redeemer = redemp["redeemer"][:10] + "..."
        
        print(f"{timestamp} | {redeemer} | {payout}")
        print(f"  Condition: {redemp['condition'][:20]}...")
        print()

def open_interest(condition_id: str = None):
    """Show open interest (total locked value)"""
    client = SubgraphClient()
    
    if condition_id:
        print(f"\n🔒 MARKET OPEN INTEREST\n")
        result = client.get_market_open_interest(condition_id)
        
        if not result or "marketOpenInterest" not in result or not result["marketOpenInterest"]:
            print("No open interest data for this market")
            return
        
        oi = result["marketOpenInterest"]
        amount = format_usdc(oi["amount"])
        print(f"Condition: {oi['id'][:30]}...")
        print(f"Open Interest: {amount}")
    
    else:
        print(f"\n🌍 GLOBAL OPEN INTEREST\n")
        result = client.get_global_open_interest()
        
        if not result or "globalOpenInterest" not in result or not result["globalOpenInterest"]:
            print("Could not fetch global open interest")
            return
        
        oi = result["globalOpenInterest"]
        amount = format_usdc(oi["amount"])
        print(f"Total Locked Value: {amount}")

def main():
    if len(sys.argv) < 2:
        print("""
Volume Analytics - Track Polymarket activity

COMMANDS:
  volume <token_id>             Show volume stats for a market
  splits [limit]                Show recent USDC splits (default: 10)
  redemptions [limit]           Show recent redemptions (default: 10)
  oi [condition_id]             Show open interest (global or by condition)

EXAMPLES:
  python3 volume_analytics.py volume 71321045679252212594626385532706912750...
  python3 volume_analytics.py splits 20
  python3 volume_analytics.py redemptions 15
  python3 volume_analytics.py oi
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "volume":
        if len(sys.argv) < 3:
            print("Error: Provide token ID")
            return
        market_volume(sys.argv[2])
    
    elif command == "splits":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        recent_splits(limit)
    
    elif command == "redemptions":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        recent_redemptions(limit)
    
    elif command == "oi":
        condition_id = sys.argv[2] if len(sys.argv) > 2 else None
        open_interest(condition_id)
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

