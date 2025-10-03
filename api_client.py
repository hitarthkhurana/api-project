"""
Polymarket API Client
Handles all API requests to CLOB and Gamma endpoints
"""

import requests
from typing import List, Dict, Optional

CLOB_API = "https://clob.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"

class PolymarketAPI:
    """Client for Polymarket REST APIs"""
    
    def search(self, query: str, limit: int = 20) -> Dict:
        """Search markets using public-search endpoint"""
        params = {
            'q': query,
            'limit_per_type': limit,
            'search_tags': 'true',
            'events_status': 'active'
        }
        response = requests.get(f"{GAMMA_API}/public-search", params=params, timeout=10)
        return response.json() if response.status_code == 200 else {}
    
    def get_active_markets(self, limit: int = 500) -> Dict:
        """Get active markets from CLOB"""
        response = requests.get(f"{CLOB_API}/sampling-markets", timeout=10)
        return response.json() if response.status_code == 200 else {}
    
    def get_market_prices(self) -> Dict:
        """Get current market prices"""
        response = requests.get(f"{CLOB_API}/sampling-simplified-markets", timeout=10)
        return response.json() if response.status_code == 200 else {}
    
    def get_all_markets(self) -> Dict:
        """Get all markets (cached)"""
        response = requests.get(f"{CLOB_API}/markets", timeout=10)
        return response.json() if response.status_code == 200 else {}
    
    def get_tags(self) -> List:
        """Get market categories/tags"""
        response = requests.get(f"{GAMMA_API}/tags", timeout=10)
        return response.json() if response.status_code == 200 else []

