#!/usr/bin/env python3
"""
Polymarket CLI - Command-line interface for Polymarket APIs
"""

import sys
from api_client import PolymarketAPI

def print_help():
    """Print help message"""
    print("""
Polymarket CLI - Query prediction markets

COMMANDS:
  search <keyword>     Search markets by keyword
  event <slug>         Get event details  
  market <id>          Get market odds/prices
  trending [limit]     Show active markets
  info                 API statistics

EXAMPLES:
  python3 polymarket_cli.py search "trump"
  python3 polymarket_cli.py market 0x80dbcce5a1e4e4a1dc
  python3 polymarket_cli.py trending 5
""")

def search_markets(api: PolymarketAPI, keyword: str):
    """Search for markets"""
    print(f"\n🔍 SEARCH: '{keyword}'")
    print("=" * 80)
    
    data = api.search(keyword)
    events = data.get('events', [])
    
    print(f"✅ Found {len(events)} events\n")
    
    for i, event in enumerate(events[:10], 1):
        title = event.get('title', 'N/A')
        slug = event.get('slug', 'N/A')
        volume = event.get('volume', 0)
        markets = event.get('markets', [])
        status = "🟢" if event.get('active') else "🔴"
        
        print(f"{i}. {status} {title}")
        print(f"   Slug: {slug}")
        print(f"   Volume: ${volume:,.0f} | Markets: {len(markets)}")
        print()

def get_event_details(api: PolymarketAPI, slug: str):
    """Get event details by slug"""
    print(f"\n📊 EVENT DETAILS")
    print("=" * 80)
    
    # Search for the event
    data = api.search(slug.replace('-', ' '))
    events = data.get('events', [])
    
    event = None
    for e in events:
        if e.get('slug') == slug:
            event = e
            break
    
    if not event and events:
        event = events[0]
    
    if event:
        print(f"\n📋 {event.get('title', 'N/A')}")
        print(f"💰 Volume: ${event.get('volume', 0):,.0f}")
        
        markets = event.get('markets', [])
        if markets:
            print(f"\n💰 Markets: {len(markets)}")
            print("-" * 80)
            
            for i, market in enumerate(markets, 1):
                question = market.get('question', 'N/A')
                condition_id = market.get('conditionId', 'N/A')
                print(f"\n{i}. {question}")
                print(f"   ID: {condition_id}")
    else:
        print(f"❌ Event not found: {slug}")

def get_market_details(api: PolymarketAPI, condition_id: str):
    """Get market odds and prices"""
    print(f"\n📊 MARKET DETAILS")
    print("=" * 80)
    
    data = api.get_market_prices()
    markets = data.get('data', [])
    
    market = None
    for m in markets:
        if condition_id in m.get('condition_id', ''):
            market = m
            break
    
    if market:
        print(f"\n🔗 {market.get('condition_id', 'N/A')}")
        
        tokens = market.get('tokens', [])
        if tokens:
            print(f"\n💰 Current Odds:")
            for token in tokens:
                outcome = token.get('outcome', 'N/A')
                price = float(token.get('price', 0))
                pct = price * 100
                implied = f"1:{1/price:.2f}" if price > 0 else "N/A"
                
                print(f"  {outcome}: {pct:.2f}% (Implied: {implied})")
    else:
        print(f"❌ Market not found: {condition_id}")

def show_trending(api: PolymarketAPI, limit: int = 10):
    """Show active markets (note: not sorted by volume like website)"""
    print(f"\n🔥 ACTIVE MARKETS")
    print("=" * 80)
    print("Note: Use search for specific topics. Trending sort not available via API.\n")
    
    data = api.get_active_markets()
    markets = data.get('data', [])
    
    active = [m for m in markets if m.get('active') and m.get('accepting_orders')][:limit]
    
    for i, market in enumerate(active, 1):
        question = market.get('question', 'N/A')
        print(f"\n{i}. {question}")
        print(f"   ID: {market.get('condition_id', 'N/A')[:30]}...")

def show_info(api: PolymarketAPI):
    """Show API info"""
    print(f"\n📊 API INFO")
    print("=" * 80)
    
    data = api.get_all_markets()
    markets = data.get('data', [])
    
    total = len(markets)
    active = len([m for m in markets if m.get('active')])
    
    print(f"\nMarkets: {total}")
    print(f"Active: {active}")
    print(f"\nAPIs: Gamma + CLOB")

def main():
    """Main entry point"""
    api = PolymarketAPI()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_help()
    elif command == "search":
        if len(sys.argv) < 3:
            print("❌ Usage: search <keyword>")
            return
        search_markets(api, " ".join(sys.argv[2:]))
    elif command == "event":
        if len(sys.argv) < 3:
            print("❌ Usage: event <slug>")
            return
        get_event_details(api, sys.argv[2])
    elif command == "market":
        if len(sys.argv) < 3:
            print("❌ Usage: market <condition_id>")
            return
        get_market_details(api, sys.argv[2])
    elif command == "trending":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        show_trending(api, limit)
    elif command == "info":
        show_info(api)
    else:
        print(f"❌ Unknown command: {command}")
        print_help()

if __name__ == "__main__":
    main()
