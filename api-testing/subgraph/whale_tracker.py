"""
Whale Tracker - Monitor large trades and positions on Polymarket
"""
import sys
from datetime import datetime
from client import SubgraphClient

def format_usdc(amount_str: str) -> str:
    """Convert USDC amount (6 decimals) to readable format"""
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

def shorten_address(addr: str) -> str:
    """Shorten Ethereum address"""
    if len(addr) > 10:
        return f"{addr[:6]}...{addr[-4:]}"
    return addr

def track_whales(min_trade: int = 1000, limit: int = 20):
    """Track large trades (whale activity)"""
    print(f"\n🐋 WHALE TRACKER - Trades over ${min_trade:,}\n")
    
    client = SubgraphClient()
    result = client.get_large_trades(min_amount=min_trade, limit=limit)
    
    if not result or "orderFilledEvents" not in result:
        print("No large trades found or API error")
        return
    
    trades = result["orderFilledEvents"]
    
    if not trades:
        print("No recent whale trades found")
        return
    
    for trade in trades:
        maker_amt = format_usdc(trade["makerAmountFilled"])
        taker_amt = format_usdc(trade["takerAmountFilled"])
        fee = format_usdc(trade["fee"])
        timestamp = format_timestamp(trade["timestamp"])
        maker = shorten_address(trade["maker"])
        taker = shorten_address(trade["taker"])
        
        print(f"{'='*70}")
        print(f"Time: {timestamp}")
        print(f"Maker: {maker} → {maker_amt}")
        print(f"Taker: {taker} → {taker_amt}")
        print(f"Fee: {fee}")
        print(f"Maker Token: {trade['makerAssetId'][:16]}...")
        print(f"Taker Token: {trade['takerAssetId'][:16]}...")

def track_user_positions(user_address: str):
    """Track specific user's positions and PnL"""
    print(f"\n💼 USER POSITIONS - {user_address}\n")
    
    client = SubgraphClient()
    result = client.get_user_positions(user_address)
    
    if not result or "userPositions" not in result:
        print("No positions found or invalid address")
        return
    
    positions = result["userPositions"]
    
    if not positions:
        print("User has no positions")
        return
    
    total_pnl = 0
    
    for pos in positions:
        amount = int(pos["amount"]) / 10**6
        avg_price = int(pos["avgPrice"]) / 10**6
        pnl = int(pos["realizedPnl"]) / 10**6
        total_bought = int(pos["totalBought"]) / 10**6
        total_pnl += pnl
        
        print(f"Token ID: {pos['tokenId']}")
        print(f"  Amount: {amount:,.2f} shares")
        print(f"  Avg Price: ${avg_price:.4f}")
        print(f"  Total Bought: {total_bought:,.2f}")
        print(f"  Realized PnL: ${pnl:,.2f}")
        print()
    
    print(f"Total Realized PnL: ${total_pnl:,.2f}")

def global_stats():
    """Show global trading statistics"""
    print("\n📊 GLOBAL TRADING STATS\n")
    
    client = SubgraphClient()
    result = client.get_global_stats()
    
    if not result or "ordersMatchedGlobal" not in result:
        print("Could not fetch global stats")
        return
    
    stats = result["ordersMatchedGlobal"]
    
    total_trades = int(stats["tradesQuantity"])
    buys = int(stats["buysQuantity"])
    sells = int(stats["sellsQuantity"])
    volume = float(stats["scaledCollateralVolume"])
    buy_volume = float(stats["scaledCollateralBuyVolume"])
    sell_volume = float(stats["scaledCollateralSellVolume"])
    
    print(f"Total Trades: {total_trades:,}")
    print(f"  Buys: {buys:,}")
    print(f"  Sells: {sells:,}")
    print(f"\nTotal Volume: ${volume:,.2f}")
    print(f"  Buy Volume: ${buy_volume:,.2f}")
    print(f"  Sell Volume: ${sell_volume:,.2f}")

def main():
    if len(sys.argv) < 2:
        print("""
Whale Tracker - Monitor large Polymarket trades

COMMANDS:
  whales [min_amount] [limit]    Show large trades (default: $1000, 20 trades)
  user <address>                 Show user positions and PnL
  stats                          Show global trading statistics

EXAMPLES:
  python3 whale_tracker.py whales 5000 10
  python3 whale_tracker.py user 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
  python3 whale_tracker.py stats
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "whales":
        min_amt = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        track_whales(min_amt, limit)
    
    elif command == "user":
        if len(sys.argv) < 3:
            print("Error: Provide user address")
            return
        track_user_positions(sys.argv[2])
    
    elif command == "stats":
        global_stats()
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

