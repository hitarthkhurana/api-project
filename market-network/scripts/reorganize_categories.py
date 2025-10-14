import json

def normalize_category(title, original_category):
    """Reorganize categories based on event title and original category"""
    title_lower = title.lower()
    cat_lower = original_category.lower()
    
    # Politics - elections, government, world leaders
    if any(x in title_lower or x in cat_lower for x in [
        "election", "president", "congress", "senate", "government", "mayoral", 
        "governor", "prime minister", "parliament", "democrat", "republican",
        "trump", "biden", "white house", "political", "sliwa", "nyc mayor"
    ]):
        return "Politics"
    
    # Sports - all major sports
    elif any(x in title_lower or x in cat_lower for x in [
        "nfl", "nba", "nhl", "mlb", "mls", "f1", "ufc", "mma", "champion",
        "super bowl", "world series", "playoffs", "vs.", " vs ", "soccer",
        "football", "baseball", "basketball", "hockey", "tennis", "golf",
        "premier league", "champions league", "la liga", "formula 1", "heisman"
    ]):
        return "Sports"
    
    # Crypto - blockchain, tokens, DeFi
    elif any(x in title_lower or x in cat_lower for x in [
        "bitcoin", "ethereum", "solana", "xrp", "crypto", "defi", "web3",
        "token", "airdrop", "nft", "metamask", "base", "hyperliquid", "monad",
        "btc", "eth", "sol", "blockchain", "fdv"
    ]):
        return "Crypto"
    
    # Entertainment - movies, music, TV, awards
    elif any(x in title_lower or x in cat_lower for x in [
        "movie", "film", "oscar", "netflix", "spotify", "album", "music",
        "taylor swift", "box office", "grammy", "emmy", "tv", "cinema",
        "song", "artist"
    ]):
        return "Entertainment"
    
    # Tech - AI, companies, startups
    elif any(x in title_lower or x in cat_lower for x in [
        " ai ", "artificial intelligence", "openai", "gpt", "gemini", "model",
        "apple", "tesla", "microsoft", "google", "meta", "amazon", "nvidia",
        "startup", "silicon", "tech", "polymarket us", "tiktok", "deepseek",
        "sora", "self driving"
    ]):
        return "Tech"
    
    # World - geopolitics, international events, wars
    elif any(x in title_lower or x in cat_lower for x in [
        "war", "ceasefire", "israel", "gaza", "hamas", "ukraine", "russia",
        "china", "taiwan", "iran", "military", "invasion", "hostage", "nuclear",
        "tariff", "nato", "strikes", "khamenei", "xi jinping", "putin",
        "maduro", "venezuela", "south korea", "north korea", "korea"
    ]):
        return "World"
    
    # Economy - markets, Fed, economic indicators
    elif any(x in title_lower or x in cat_lower for x in [
        "fed", "interest rate", "inflation", "recession", "gdp", "unemployment",
        "richest person", "largest company", "shutdown", "funding bill",
        "economy", "economic", "fiscal", "monetary", "ecb", "cpi", "gold",
        "jerome powell", "earnings", "quarterly", "stock", "nyse", "macro"
    ]):
        return "Economy"
    
    # Culture - celebrities, pop culture, social media, esports
    elif any(x in title_lower or x in cat_lower for x in [
        "celebrity", "kardashian", "mrbeast", "influencer", "viral", "youtube",
        "instagram", "views", "pewdiepie", "lol", "counter-strike", "esports",
        "gaming", "person of the year", "pregnant", "aliens", "pope", "love is blind",
        "fact check", "climate", "temperature", "2025 predictions"
    ]):
        return "Culture"
    
    # Keep original if it doesn't match any pattern
    else:
        return original_category

def main():
    # Read network.json
    with open("../public/network.json", "r") as f:
        data = json.load(f)
    
    print(f"📊 Original categories:")
    category_counts = {}
    for node in data["nodes"]:
        cat = node["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    # Reorganize categories
    for node in data["nodes"]:
        old_cat = node["category"]
        new_cat = normalize_category(node["label"], old_cat)
        node["category"] = new_cat
    
    print(f"\n✨ New categories:")
    new_category_counts = {}
    for node in data["nodes"]:
        cat = node["category"]
        new_category_counts[cat] = new_category_counts.get(cat, 0) + 1
    
    for cat, count in sorted(new_category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    # Write back to network.json
    with open("../public/network.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Updated network.json with reorganized categories!")

if __name__ == "__main__":
    main()

