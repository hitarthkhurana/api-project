"""
Liquidity Analyzer - Order book depth and slippage estimation
"""
import sys
import requests

CLOB_API = "https://clob.polymarket.com"

def get_order_book(token_id: str):
    """Fetch order book for a token"""
    try:
        response = requests.get(f"{CLOB_API}/book", params={"token_id": token_id}, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching order book: {e}")
        return None

def analyze_depth(token_id: str, levels: int = 10):
    """Analyze order book depth at different price levels"""
    print(f"\n📊 LIQUIDITY DEPTH ANALYSIS\n")
    print(f"Token: {token_id[:20]}...\n")
    
    book = get_order_book(token_id)
    if not book:
        return
    
    bids = book.get("bids", [])[:levels]
    asks = book.get("asks", [])[:levels]
    
    print(f"{'BIDS (Buy Orders)':<40} | {'ASKS (Sell Orders)'}")
    print(f"{'Price':<12} {'Size':<12} {'Total':<12} | {'Price':<12} {'Size':<12} {'Total'}")
    print("=" * 85)
    
    bid_total = 0
    ask_total = 0
    
    max_rows = max(len(bids), len(asks))
    
    for i in range(max_rows):
        # Bid side
        if i < len(bids):
            bid = bids[i]
            bid_price = float(bid["price"])
            bid_size = float(bid["size"])
            bid_total += bid_size
            bid_str = f"${bid_price:<11.4f} {bid_size:<11.2f} {bid_total:<11.2f}"
        else:
            bid_str = " " * 37
        
        # Ask side
        if i < len(asks):
            ask = asks[i]
            ask_price = float(ask["price"])
            ask_size = float(ask["size"])
            ask_total += ask_size
            ask_str = f"${ask_price:<11.4f} {ask_size:<11.2f} {ask_total:<11.2f}"
        else:
            ask_str = ""
        
        print(f"{bid_str} | {ask_str}")
    
    # Calculate spread
    if bids and asks:
        best_bid = float(bids[0]["price"])
        best_ask = float(asks[0]["price"])
        spread = best_ask - best_bid
        spread_pct = (spread / best_ask) * 100 if best_ask > 0 else 0
        
        print(f"\n{'='*85}")
        print(f"Best Bid: ${best_bid:.4f} | Best Ask: ${best_ask:.4f}")
        print(f"Spread: ${spread:.4f} ({spread_pct:.2f}%)")
        print(f"Total Bid Liquidity: {bid_total:.2f} shares")
        print(f"Total Ask Liquidity: {ask_total:.2f} shares")

def calculate_slippage(token_id: str, trade_size: float, side: str = "BUY"):
    """Calculate slippage for a given trade size"""
    print(f"\n💹 SLIPPAGE CALCULATOR\n")
    print(f"Trade: {side} {trade_size:.2f} shares\n")
    
    book = get_order_book(token_id)
    if not book:
        return
    
    # Choose bids or asks based on side
    orders = book.get("asks" if side == "BUY" else "bids", [])
    
    if not orders:
        print("No liquidity available")
        return
    
    remaining = trade_size
    total_cost = 0
    fills = []
    
    for order in orders:
        price = float(order["price"])
        size = float(order["size"])
        
        if remaining <= 0:
            break
        
        fill_size = min(remaining, size)
        fill_cost = fill_size * price
        
        fills.append({
            "price": price,
            "size": fill_size,
            "cost": fill_cost
        })
        
        total_cost += fill_cost
        remaining -= fill_size
    
    if remaining > 0:
        print(f"⚠️  Insufficient liquidity! {remaining:.2f} shares unfilled\n")
    
    avg_price = total_cost / (trade_size - remaining) if (trade_size - remaining) > 0 else 0
    best_price = float(orders[0]["price"])
    slippage = avg_price - best_price
    slippage_pct = (slippage / best_price) * 100 if best_price > 0 else 0
    
    print(f"{'Price':<12} {'Size':<12} {'Cost':<12}")
    print("=" * 40)
    for fill in fills:
        print(f"${fill['price']:<11.4f} {fill['size']:<11.2f} ${fill['cost']:<11.2f}")
    
    print("\n" + "=" * 40)
    print(f"Best Price: ${best_price:.4f}")
    print(f"Average Fill Price: ${avg_price:.4f}")
    print(f"Slippage: ${slippage:.4f} ({slippage_pct:.2f}%)")
    print(f"Total Cost: ${total_cost:.2f}")
    
    if remaining == 0:
        print(f"✅ Full fill achieved")
    else:
        print(f"⚠️  Partial fill: {trade_size - remaining:.2f} / {trade_size:.2f} shares")

def main():
    if len(sys.argv) < 2:
        print("""
Liquidity Analyzer - Order book depth and slippage

COMMANDS:
  depth <token_id> [levels]          Show order book depth (default: 10 levels)
  slippage <token_id> <size> [side]  Calculate slippage (default: BUY)

EXAMPLES:
  python3 liquidity_analyzer.py depth 71321045679252212594626385532706912750...
  python3 liquidity_analyzer.py slippage 71321045679252212594626385532706912750... 100
  python3 liquidity_analyzer.py slippage 71321045679252212594626385532706912750... 500 SELL
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "depth":
        if len(sys.argv) < 3:
            print("Error: Provide token ID")
            return
        token_id = sys.argv[2]
        levels = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        analyze_depth(token_id, levels)
    
    elif command == "slippage":
        if len(sys.argv) < 4:
            print("Error: Provide token ID and trade size")
            return
        token_id = sys.argv[2]
        size = float(sys.argv[3])
        side = sys.argv[4].upper() if len(sys.argv) > 4 else "BUY"
        calculate_slippage(token_id, size, side)
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

