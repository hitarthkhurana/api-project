#!/usr/bin/env python3
"""
Market WebSocket Stream - Initial Implementation
Connects to CLOB WebSocket for real-time market data
"""

import websocket
import json
import time

WS_URL = "wss://ws-subscriptions-clob.polymarket.com/ws/market"

def on_message(ws, message):
    """Handle incoming messages"""
    if message == "PONG":
        return
    
    try:
        data = json.loads(message)
        event_type = data.get('event_type')
        
        if event_type == 'book':
            # Order book update
            asset_id = data.get('asset_id', 'N/A')[:20]
            bids = data.get('bids', [])
            asks = data.get('asks', [])
            print(f"\n📊 BOOK UPDATE - Asset: {asset_id}...")
            if bids:
                print(f"   Best Bid: ${bids[0]['price']} x {bids[0]['size']}")
            if asks:
                print(f"   Best Ask: ${asks[0]['price']} x {asks[0]['size']}")
                
        elif event_type == 'price_change':
            # Price change
            market = data.get('market', 'N/A')[:20]
            changes = data.get('price_changes', [])
            print(f"\n💹 PRICE CHANGE - Market: {market}...")
            for change in changes[:2]:
                side = change.get('side')
                price = change.get('price')
                size = change.get('size')
                print(f"   {side}: ${price} x {size}")
                
    except json.JSONDecodeError:
        print(f"Non-JSON: {message}")

def on_error(ws, error):
    """Handle errors"""
    print(f"❌ Error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Handle close"""
    print("\n🔴 Connection closed")

def on_open(ws):
    """Handle connection open"""
    print("🟢 Connected to Market WebSocket")
    
    # Subscribe to a market (Trump election market example)
    # Asset ID format: token ID for a specific outcome
    subscribe_msg = {
        "assets_ids": [
            "71321045679252212594626385532706912750332728571942532289631379312455583992563"
        ],
        "type": "market"
    }
    
    ws.send(json.dumps(subscribe_msg))
    print("📡 Subscribed to market updates\n")

def main():
    """Entry point"""
    print("=" * 80)
    print("POLYMARKET CLOB WEBSOCKET - MARKET STREAM")
    print("=" * 80)
    print()
    
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    try:
        ws.run_forever()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stream stopped")

if __name__ == "__main__":
    main()

