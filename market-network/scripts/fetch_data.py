import requests
import json

GAMMA_API = "https://gamma-api.polymarket.com"
PNL_SUBGRAPH = "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/pnl-subgraph/0.0.14/gn"

def get_active_events(limit=50):
    print(f"Fetching {limit} active events...")
    
    response = requests.get(
        f"{GAMMA_API}/events",
        params={"closed": "false", "limit": limit, "order": "volume24hr", "ascending": "false"},
        timeout=15
    )
    events = response.json()
    
    events_data = []
    for event in events:
        token_ids = []
        total_volume = 0
        
        for market in event.get("markets", []):
            clob_ids = json.loads(market.get("clobTokenIds", "[]"))
            token_ids.extend(clob_ids)
            total_volume += float(market.get("volumeNum", 0))
        
        if token_ids and total_volume > 5000:
            tags = event.get("tags", [])
            category = tags[0].get("label", "Other") if tags else "Other"
            
            events_data.append({
                "title": event.get("title", "Unknown"),
                "slug": event.get("slug", ""),
                "category": category,
                "token_ids": token_ids,
                "volume": total_volume
            })
    
    print(f"Got {len(events_data)} events with >$5k volume")
    return events_data

def get_traders(token_id):
    query = f'''
    {{
      userPositions(where: {{tokenId: "{token_id}"}}, first: 1000) {{
        user
      }}
    }}
    '''
    
    try:
        response = requests.post(PNL_SUBGRAPH, json={"query": query}, timeout=10)
        positions = response.json()["data"]["userPositions"]
        return set([p["user"] for p in positions])
    except:
        return set()

def get_all_traders_for_event(token_ids):
    """Get union of all traders across all markets in an event"""
    all_traders = set()
    
    for token_id in token_ids:
        traders = get_traders(token_id)
        all_traders.update(traders)
    
    return all_traders

def calculate_overlaps(events_data):
    print("Fetching trader positions for each event...")
    
    event_traders = {}
    for i, event in enumerate(events_data, 1):
        traders = get_all_traders_for_event(event["token_ids"])
        if traders:
            event_traders[event["slug"]] = traders
            print(f"  {i}/{len(events_data)}: {event['title'][:40]}... → {len(traders)} traders")
    
    print(f"\nCalculating overlaps between {len(event_traders)} events...")
    
    edges = []
    slugs = list(event_traders.keys())
    
    for i, slug_a in enumerate(slugs):
        for slug_b in slugs[i+1:]:
            traders_a = event_traders[slug_a]
            traders_b = event_traders[slug_b]
            
            overlap = len(traders_a & traders_b)
            total = len(traders_a | traders_b)
            overlap_pct = (overlap / total * 100) if total > 0 else 0
            
            if overlap_pct > 5:
                edges.append({
                    "source": slug_a,
                    "target": slug_b,
                    "weight": round(overlap_pct, 1)
                })
    
    return event_traders, edges

def main():
    events_data = get_active_events(50)
    event_traders, edges = calculate_overlaps(events_data)
    
    nodes = []
    for event in events_data:
        slug = event["slug"]
        if slug in event_traders:
            nodes.append({
                "id": slug,
                "label": event["title"],
                "category": event["category"],
                "traders": len(event_traders[slug]),
                "volume": event["volume"]
            })
    
    network = {
        "nodes": nodes,
        "edges": edges
    }
    
    with open("../public/network.json", "w") as f:
        json.dump(network, f, indent=2)
    
    total_vol = sum(n["volume"] for n in nodes)
    print(f"\n✓ network.json")
    print(f"  {len(nodes)} events")
    print(f"  {len(edges)} connections")
    print(f"  ${total_vol:,.0f} volume")

if __name__ == "__main__":
    main()
