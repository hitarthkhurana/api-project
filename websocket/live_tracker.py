#!/usr/bin/env python3
"""
Live Market Tracker - Enhanced WebSocket Implementation
Real-time tracking with price analytics and spread monitoring
"""

import websocket
import json
import time
import threading
from datetime import datetime

WS_URL = "wss://ws-subscriptions-clob.polymarket.com/ws/market"

class LiveMarketTracker:
    """Enhanced market tracker with analytics"""
    
    def __init__(self, asset_ids):
        self.asset_ids = asset_ids
        self.ws = None
        self.books = {}  # Store order books
        self.price_history = {}  # Track price changes
        self.last_update = {}
        
    def calculate_spread(self, bids, asks):
        """Calculate bid-ask spread"""
        if not bids or not asks:
            return None
        
        best_bid = float(bids[0]['price'])
        best_ask = float(asks[0]['price'])
        spread = best_ask - best_bid
        spread_pct = (spread / best_ask) * 100 if best_ask > 0 else 0
        
        return {
            'spread': spread,
            'spread_pct': spread_pct,
            'mid_price': (best_bid + best_ask) / 2
        }
    
    def on_message(self, ws, message):
        """Handle incoming messages"""
        if message in ["PONG", "PING"]:
            return
        
        try:
            data = json.loads(message)
            event_type = data.get('event_type')
            
            if event_type == 'book':
                self.handle_book_update(data)
            elif event_type == 'price_change':
                self.handle_price_change(data)
            elif event_type == 'last_trade_price':
                self.handle_last_trade(data)
                
        except json.JSONDecodeError:
            pass
    
    def handle_book_update(self, data):
        """Process order book update"""
        asset_id = data.get('asset_id', '')[:16]
        bids = data.get('bids', [])
        asks = data.get('asks', [])
        
        self.books[asset_id] = {'bids': bids, 'asks': asks}
        
        spread_info = self.calculate_spread(bids, asks)
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{timestamp}] 📊 ORDER BOOK - {asset_id}...")
        
        if bids:
            print(f"   Best Bid: ${float(bids[0]['price']):.3f} ({bids[0]['size']} shares)")
        if asks:
            print(f"   Best Ask: ${float(asks[0]['price']):.3f} ({asks[0]['size']} shares)")
        
        if spread_info:
            print(f"   Spread: ${spread_info['spread']:.4f} ({spread_info['spread_pct']:.2f}%)")
            print(f"   Mid Price: ${spread_info['mid_price']:.3f}")
    
    def handle_price_change(self, data):
        """Process price change event"""
        market = data.get('market', '')[:16]
        changes = data.get('price_changes', [])
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{timestamp}] 💹 PRICE CHANGE - {market}...")
        
        for change in changes[:3]:
            asset_id = change.get('asset_id', '')[:16]
            side = change.get('side')
            price = float(change.get('price', 0))
            size = float(change.get('size', 0))
            
            # Track price history
            if asset_id not in self.price_history:
                self.price_history[asset_id] = []
            self.price_history[asset_id].append({
                'timestamp': time.time(),
                'side': side,
                'price': price,
                'size': size
            })
            
            # Keep only last 10 price points
            self.price_history[asset_id] = self.price_history[asset_id][-10:]
            
            print(f"   {side}: ${price:.3f} x {size:.0f} shares")
    
    def handle_last_trade(self, data):
        """Process last trade event"""
        asset_id = data.get('asset_id', '')[:16]
        price = float(data.get('price', 0))
        size = float(data.get('size', 0))
        side = data.get('side', 'N/A')
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{timestamp}] 🔥 TRADE EXECUTED - {asset_id}...")
        print(f"   Side: {side} | Price: ${price:.3f} | Size: {size:.2f}")
    
    def on_error(self, ws, error):
        """Handle errors"""
        print(f"\n❌ Error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Handle connection close"""
        print(f"\n🔴 Connection closed")
    
    def on_open(self, ws):
        """Handle connection open"""
        print("🟢 Connected to CLOB Market WebSocket")
        
        subscribe_msg = {
            "assets_ids": self.asset_ids,
            "type": "market"
        }
        
        ws.send(json.dumps(subscribe_msg))
        print(f"📡 Tracking {len(self.asset_ids)} market(s)\n")
        print("=" * 80)
        
        # Start ping thread
        def send_ping():
            while True:
                time.sleep(5)
                try:
                    ws.send("PING")
                except:
                    break
        
        ping_thread = threading.Thread(target=send_ping, daemon=True)
        ping_thread.start()
    
    def start(self):
        """Start WebSocket connection"""
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            WS_URL,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        self.ws.run_forever()

def main():
    """Entry point"""
    print("=" * 80)
    print("POLYMARKET LIVE MARKET TRACKER")
    print("Real-time Order Book, Prices, and Trade Analytics")
    print("=" * 80)
    print()
    
    # Example: Track multiple popular markets
    # These are token IDs for different market outcomes
    markets = [
        "71321045679252212594626385532706912750332728571942532289631379312455583992563",  # Example market 1
        "52114319501245915516055106046884209969926127482827954674443846427813813222426",  # Example market 2
    ]
    
    tracker = LiveMarketTracker(markets)
    
    try:
        tracker.start()
    except KeyboardInterrupt:
        print("\n\n⏹️  Tracker stopped\n")
        
        # Print summary
        print("=" * 80)
        print("SESSION SUMMARY")
        print("=" * 80)
        print(f"Markets tracked: {len(tracker.books)}")
        print(f"Price updates: {sum(len(h) for h in tracker.price_history.values())}")

if __name__ == "__main__":
    main()

