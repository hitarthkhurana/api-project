"""
Top Markets - Find most active markets by volume and trades
"""
import sys
import requests

def format_volume(amount: str) -> str:
    """Format volume to readable string"""
    try:
        vol = float(amount)
        if vol >= 1_000_000:
            return f"${vol/1_000_000:.2f}M"
        elif vol >= 1_000:
            return f"${vol/1_000:.2f}K"
        else:
            return f"${vol:.2f}"
    except:
        return amount

def top_markets_by_volume(limit: int = 20):
    """Find top markets by total volume"""
    print(f"\n📈 TOP {limit} MARKETS BY VOLUME\n")
    
    query = """
    query($limit: Int!) {
      orderbooks(
        first: $limit
        orderBy: scaledCollateralVolume
        orderDirection: desc
        where: {scaledCollateralVolume_gt: 0}
      ) {
        id
        tradesQuantity
        buysQuantity
        sellsQuantity
        scaledCollateralVolume
        scaledCollateralBuyVolume
        scaledCollateralSellVolume
      }
    }
    """
    
    payload = {"query": query, "variables": {"limit": limit}}
    response = requests.post(
        "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/orderbook-subgraph/0.0.1/gn",
        json=payload,
        timeout=15
    )
    data = response.json().get("data", {})
    
    if not data or "orderbooks" not in data:
        print("No markets found")
        return
    
    markets = data["orderbooks"]
    
    print(f"{'Rank':<6} {'Token ID':<20} {'Volume':<12} {'Trades':<10} {'Buy/Sell Ratio'}")
    print("=" * 80)
    
    for i, market in enumerate(markets, 1):
        token_id = market["id"][:18] + "..."
        volume = format_volume(market["scaledCollateralVolume"])
        trades = int(market["tradesQuantity"])
        buys = int(market["buysQuantity"])
        sells = int(market["sellsQuantity"])
        
        ratio = f"{buys}/{sells}" if sells > 0 else f"{buys}/0"
        
        print(f"{i:<6} {token_id:<20} {volume:<12} {trades:<10,} {ratio}")

def top_markets_by_trades(limit: int = 20):
    """Find most actively traded markets"""
    print(f"\n🔥 TOP {limit} MARKETS BY TRADE COUNT\n")
    
    query = """
    query($limit: Int!) {
      orderbooks(
        first: $limit
        orderBy: tradesQuantity
        orderDirection: desc
        where: {tradesQuantity_gt: 0}
      ) {
        id
        tradesQuantity
        buysQuantity
        sellsQuantity
        scaledCollateralVolume
      }
    }
    """
    
    payload = {"query": query, "variables": {"limit": limit}}
    response = requests.post(
        "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/orderbook-subgraph/0.0.1/gn",
        json=payload,
        timeout=15
    )
    data = response.json().get("data", {})
    
    if not data or "orderbooks" not in data:
        print("No markets found")
        return
    
    markets = data["orderbooks"]
    
    print(f"{'Rank':<6} {'Token ID':<20} {'Trades':<10} {'Volume':<12} {'Avg Trade'}")
    print("=" * 75)
    
    for i, market in enumerate(markets, 1):
        token_id = market["id"][:18] + "..."
        trades = int(market["tradesQuantity"])
        volume = float(market["scaledCollateralVolume"])
        avg_trade = volume / trades if trades > 0 else 0
        
        vol_str = format_volume(str(volume))
        avg_str = f"${avg_trade:.2f}"
        
        print(f"{i:<6} {token_id:<20} {trades:<10,} {vol_str:<12} {avg_str}")

def main():
    if len(sys.argv) < 2:
        print("""
Top Markets - Most active prediction markets

COMMANDS:
  volume [limit]    Top markets by volume (default: 20)
  trades [limit]    Top markets by trade count (default: 20)

EXAMPLES:
  python3 top_markets.py volume 10
  python3 top_markets.py trades 15
        """)
        return
    
    command = sys.argv[1].lower()
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    if command == "volume":
        top_markets_by_volume(limit)
    elif command == "trades":
        top_markets_by_trades(limit)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

