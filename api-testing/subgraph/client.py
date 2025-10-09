"""
Polymarket Subgraph Client - Query on-chain data via GraphQL
"""
import requests
import json

# Goldsky-hosted subgraph endpoints
ORDERS_SUBGRAPH = "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/orderbook-subgraph/0.0.1/gn"
POSITIONS_SUBGRAPH = "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/positions-subgraph/0.0.7/gn"
ACTIVITY_SUBGRAPH = "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/activity-subgraph/0.0.4/gn"
OI_SUBGRAPH = "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/oi-subgraph/0.0.6/gn"
PNL_SUBGRAPH = "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/pnl-subgraph/0.0.14/gn"


class SubgraphClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def query(self, endpoint: str, query: str, variables: dict = None):
        """Execute GraphQL query against specified endpoint"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        try:
            response = self.session.post(endpoint, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"GraphQL errors: {data['errors']}")
                return None
            
            return data.get("data")
        except Exception as e:
            print(f"Query failed: {e}")
            return None
    
    # === ORDERS SUBGRAPH ===
    
    def get_large_trades(self, min_amount: int = 10000, limit: int = 20):
        """Get recent large trades (whale activity)"""
        query = """
        query($minAmount: BigInt!, $limit: Int!) {
          orderFilledEvents(
            first: $limit
            orderBy: timestamp
            orderDirection: desc
            where: {makerAmountFilled_gte: $minAmount}
          ) {
            id
            timestamp
            maker
            taker
            makerAssetId
            takerAssetId
            makerAmountFilled
            takerAmountFilled
            fee
          }
        }
        """
        return self.query(
            ORDERS_SUBGRAPH,
            query,
            {"minAmount": str(min_amount * 10**6), "limit": limit}
        )
    
    def get_market_volume(self, token_id: str):
        """Get volume stats for a specific market"""
        query = """
        query($tokenId: ID!) {
          orderbook(id: $tokenId) {
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
        return self.query(ORDERS_SUBGRAPH, query, {"tokenId": token_id})
    
    def get_global_stats(self):
        """Get global trading statistics"""
        query = """
        query {
          ordersMatchedGlobal(id: "") {
            tradesQuantity
            buysQuantity
            sellsQuantity
            scaledCollateralVolume
            scaledCollateralBuyVolume
            scaledCollateralSellVolume
          }
        }
        """
        return self.query(ORDERS_SUBGRAPH, query)
    
    # === PNL SUBGRAPH ===
    
    def get_user_positions(self, user_address: str, limit: int = 10):
        """Get user's positions with PnL data"""
        query = """
        query($user: String!, $limit: Int!) {
          userPositions(
            first: $limit
            where: {user: $user}
            orderBy: amount
            orderDirection: desc
          ) {
            id
            tokenId
            amount
            avgPrice
            realizedPnl
            totalBought
          }
        }
        """
        return self.query(PNL_SUBGRAPH, query, {"user": user_address.lower(), "limit": limit})
    
    def get_top_holders(self, token_id: str, limit: int = 10):
        """Get largest holders of a specific outcome token"""
        query = """
        query($tokenId: BigInt!, $limit: Int!) {
          userPositions(
            first: $limit
            where: {tokenId: $tokenId}
            orderBy: amount
            orderDirection: desc
          ) {
            user
            amount
            avgPrice
            realizedPnl
          }
        }
        """
        return self.query(PNL_SUBGRAPH, query, {"tokenId": token_id, "limit": limit})
    
    # === ACTIVITY SUBGRAPH ===
    
    def get_recent_splits(self, limit: int = 10):
        """Get recent on-chain split events (USDC → outcome tokens)"""
        query = """
        query($limit: Int!) {
          splits(first: $limit, orderBy: timestamp, orderDirection: desc) {
            id
            timestamp
            stakeholder
            condition
            amount
          }
        }
        """
        return self.query(ACTIVITY_SUBGRAPH, query, {"limit": limit})
    
    def get_recent_redemptions(self, limit: int = 10):
        """Get recent redemptions (outcome tokens → USDC)"""
        query = """
        query($limit: Int!) {
          redemptions(first: $limit, orderBy: timestamp, orderDirection: desc) {
            id
            timestamp
            redeemer
            condition
            payout
          }
        }
        """
        return self.query(ACTIVITY_SUBGRAPH, query, {"limit": limit})
    
    # === OPEN INTEREST SUBGRAPH ===
    
    def get_market_open_interest(self, condition_id: str):
        """Get open interest for a specific market"""
        query = """
        query($conditionId: ID!) {
          marketOpenInterest(id: $conditionId) {
            id
            amount
          }
        }
        """
        return self.query(OI_SUBGRAPH, query, {"conditionId": condition_id})
    
    def get_global_open_interest(self):
        """Get total open interest across all markets"""
        query = """
        query {
          globalOpenInterest(id: "") {
            amount
          }
        }
        """
        return self.query(OI_SUBGRAPH, query)

