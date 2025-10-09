#!/usr/bin/env python3
"""
RTDS Comments Stream - Real-time comment monitoring
WebSocket connection to wss://ws-live-data.polymarket.com
"""

import json
import websocket
import time
import sys

RTDS_URL = "wss://ws-live-data.polymarket.com"

class CommentsStream:
    """Monitor real-time comments on Polymarket"""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.ws = None
        self.running = False
    
    def on_message(self, ws, message):
        """Handle incoming messages"""
        try:
            data = json.loads(message)
            
            if data.get('topic') == 'comments':
                self.handle_comment(data)
        except json.JSONDecodeError:
            if self.verbose:
                print(f"Non-JSON message: {message}")
    
    def handle_comment(self, data):
        """Process comment event"""
        msg_type = data.get('type')
        payload = data.get('payload', {})
        
        if msg_type == 'comment_created':
            username = payload.get('profile', {}).get('name', 'Anonymous')
            body = payload.get('body', '')
            entity_type = payload.get('parentEntityType', 'Unknown')
            entity_id = payload.get('parentEntityID', 'N/A')
            
            print(f"\n💬 NEW COMMENT")
            print(f"   User: {username}")
            print(f"   On: {entity_type} #{entity_id}")
            print(f"   Text: {body[:100]}...")
            
        elif msg_type == 'reaction_created':
            print(f"\n👍 REACTION on comment {payload.get('commentID')}")
    
    def on_error(self, ws, error):
        """Handle errors"""
        print(f"❌ Error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Handle connection close"""
        print(f"\n🔴 Connection closed")
        self.running = False
    
    def on_open(self, ws):
        """Handle connection open"""
        print("🟢 Connected to RTDS")
        
        # Subscribe to comments
        subscribe_msg = {
            "action": "subscribe",
            "subscriptions": [
                {
                    "topic": "comments",
                    "type": "comment_created"
                }
            ]
        }
        
        ws.send(json.dumps(subscribe_msg))
        print("📡 Subscribed to comments stream\n")
        print("Waiting for comments...\n")
        
        self.running = True
    
    def start(self):
        """Start WebSocket connection"""
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            RTDS_URL,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        self.ws.run_forever()

def main():
    """Entry point"""
    print("=" * 80)
    print("POLYMARKET RTDS - REAL-TIME COMMENTS STREAM")
    print("=" * 80)
    print()
    
    stream = CommentsStream(verbose=True)
    
    try:
        stream.start()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stream stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()

