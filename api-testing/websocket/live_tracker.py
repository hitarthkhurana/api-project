#!/usr/bin/env python3
"""
Live Market Tracker - Real-time order book and trade monitoring
"""

import websocket
import json
import time
import threading
from datetime import datetime

WS_URL = "wss://ws-subscriptions-clob.polymarket.com/ws/market"

class LiveMarketTracker:
    """Real-time market tracker with spread analytics"""
    
    def __init__(self, asset_ids):
        self.asset_ids = asset_ids
        self.ws = None
        self.books = {}
        self.price_history = {}
        
    def calculate_spread(self, bids, asks):
        """Calculate bid-ask spread and mid price"""
        if not bids or not asks:
            return None
        bid, ask = float(bids[0]['price']), float(asks[0]['price'])
        spread = ask - bid
        return {
            'spread': spread,
            'spread_pct': (spread / ask) * 100,
            'mid_price': (bid + ask) / 2
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
        bids, asks = data.get('bids', []), data.get('asks', [])
        self.books[asset_id] = {'bids': bids, 'asks': asks}
        
        ts = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{ts}] 📊 ORDER BOOK - {asset_id}...")
        
        if bids:
            print(f"   Bid: ${float(bids[0]['price']):.3f} x {bids[0]['size']}")
        if asks:
            print(f"   Ask: ${float(asks[0]['price']):.3f} x {asks[0]['size']}")
        
        if spread := self.calculate_spread(bids, asks):
            print(f"   Spread: ${spread['spread']:.4f} ({spread['spread_pct']:.2f}%) | Mid: ${spread['mid_price']:.3f}")
    
    def handle_price_change(self, data):
        """Process price change event"""
        market = data.get('market', '')[:16]
        ts = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{ts}] 💹 PRICE CHANGE - {market}...")
        
        for change in data.get('price_changes', [])[:3]:
            side, price, size = change.get('side'), float(change.get('price', 0)), float(change.get('size', 0))
            print(f"   {side}: ${price:.3f} x {size:.0f}")
    
    def handle_last_trade(self, data):
        """Process last trade event"""
        asset_id = data.get('asset_id', '')[:16]
        price, size, side = float(data.get('price', 0)), float(data.get('size', 0)), data.get('side', 'N/A')
        ts = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{ts}] 🔥 TRADE - {asset_id}... | {side} ${price:.3f} x {size:.2f}")
    
    def on_error(self, ws, error):
        """Handle errors"""
        print(f"\n❌ Error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Handle connection close"""
        print(f"\n🔴 Connection closed")
    
    def on_open(self, ws):
        """Handle connection open"""
        print("🟢 Connected to CLOB WebSocket")
        ws.send(json.dumps({"assets_ids": self.asset_ids, "type": "market"}))
        print(f"📡 Tracking {len(self.asset_ids)} market(s)\n" + "=" * 80)
        
        # Ping thread for connection stability
        def ping_loop():
            while True:
                time.sleep(5)
                try: ws.send("PING")
                except: break
        threading.Thread(target=ping_loop, daemon=True).start()
    
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
    print("POLYMARKET LIVE TRACKER - Real-time Order Book & Trades")
    print("=" * 80 + "\n")
    
    # Track multiple markets (token IDs)
    markets = [
        "71321045679252212594626385532706912750332728571942532289631379312455583992563",
        "52114319501245915516055106046884209969926127482827954674443846427813813222426",
    ]
    
    tracker = LiveMarketTracker(markets)
    
    try:
        tracker.start()
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Stopped | Markets tracked: {len(tracker.books)}")

if __name__ == "__main__":
    main()

