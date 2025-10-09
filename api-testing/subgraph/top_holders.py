"""
Top Holders - Find largest positions and analyze concentration
"""
import sys
from client import SubgraphClient

def format_amount(amount_str: str) -> str:
    """Convert amount to readable format"""
    try:
        amount = int(amount_str) / 10**6
        return f"{amount:,.2f}"
    except:
        return amount_str

def shorten_address(addr: str) -> str:
    """Shorten Ethereum address"""
    if len(addr) > 10:
        return f"{addr[:6]}...{addr[-4:]}"
    return addr

def top_holders_for_token(token_id: str, limit: int = 20):
    """Show largest holders of a specific outcome token"""
    print(f"\n👑 TOP {limit} HOLDERS\n")
    print(f"Token: {token_id}\n")
    
    client = SubgraphClient()
    result = client.get_top_holders(token_id, limit)
    
    if not result or "userPositions" not in result:
        print("No holders found")
        return
    
    positions = result["userPositions"]
    
    if not positions:
        print("No positions found for this token")
        return
    
    total_amount = sum(int(p["amount"]) for p in positions)
    
    print(f"{'Rank':<6} {'Address':<18} {'Amount':<15} {'% of Top {limit}':<12} {'Avg Price':<12} {'PnL'}")
    print("=" * 90)
    
    for i, pos in enumerate(positions, 1):
        address = shorten_address(pos["user"])
        amount = int(pos["amount"]) / 10**6
        avg_price = int(pos["avgPrice"]) / 10**6
        pnl = int(pos["realizedPnl"]) / 10**6
        
        pct = (int(pos["amount"]) / total_amount * 100) if total_amount > 0 else 0
        
        pnl_str = f"${pnl:+,.2f}" if pnl != 0 else "$0.00"
        
        print(f"{i:<6} {address:<18} {amount:<15,.2f} {pct:<11.1f}% ${avg_price:<11.4f} {pnl_str}")
    
    print(f"\n{'='*90}")
    print(f"Total (top {limit}): {total_amount/10**6:,.2f} shares")

def concentration_analysis(token_id: str):
    """Analyze holder concentration (whale dominance)"""
    print(f"\n📊 CONCENTRATION ANALYSIS\n")
    print(f"Token: {token_id}\n")
    
    client = SubgraphClient()
    
    # Get top 50 holders
    result = client.get_top_holders(token_id, 50)
    
    if not result or "userPositions" not in result:
        print("No data available")
        return
    
    positions = result["userPositions"]
    
    if len(positions) < 5:
        print("Insufficient data for concentration analysis")
        return
    
    total = sum(int(p["amount"]) for p in positions)
    
    # Calculate concentration metrics
    top_1 = int(positions[0]["amount"]) if len(positions) >= 1 else 0
    top_5 = sum(int(p["amount"]) for p in positions[:5]) if len(positions) >= 5 else 0
    top_10 = sum(int(p["amount"]) for p in positions[:10]) if len(positions) >= 10 else 0
    top_20 = sum(int(p["amount"]) for p in positions[:20]) if len(positions) >= 20 else 0
    
    print(f"Top 1 holder: {top_1/total*100:.1f}% of top 50")
    print(f"Top 5 holders: {top_5/total*100:.1f}% of top 50")
    print(f"Top 10 holders: {top_10/total*100:.1f}% of top 50")
    print(f"Top 20 holders: {top_20/total*100:.1f}% of top 50")
    
    # Interpret concentration
    top_5_pct = top_5/total*100
    
    print(f"\n{'='*50}")
    if top_5_pct > 70:
        print("⚠️  HIGH concentration - Market dominated by whales")
    elif top_5_pct > 50:
        print("📈 MODERATE concentration - Some whale influence")
    else:
        print("✅ LOW concentration - More distributed market")

def main():
    if len(sys.argv) < 2:
        print("""
Top Holders - Analyze token holder distribution

COMMANDS:
  holders <token_id> [limit]     Show top holders (default: 20)
  concentration <token_id>       Analyze holder concentration

EXAMPLES:
  python3 top_holders.py holders 71321045679252212594626385532706912750... 10
  python3 top_holders.py concentration 71321045679252212594626385532706912750...
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "holders":
        if len(sys.argv) < 3:
            print("Error: Provide token ID")
            return
        token_id = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        top_holders_for_token(token_id, limit)
    
    elif command == "concentration":
        if len(sys.argv) < 3:
            print("Error: Provide token ID")
            return
        token_id = sys.argv[2]
        concentration_analysis(token_id)
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

