from eatnyc import load_data, top_n, filter_restaurants, format_card # add others as they land

def main():
    data = load_data()
    print("rows:", len(data))
    
    # === Top restaurants by rating ===
    print("\n=== Top 5 by rating (simple print) ===")
    for r in top_n(data, n=5):
        print(f"- {r['name']} ({r['cuisine']}, {r['price']}) ★ {r['rating']} – {r['sample_dish']}")

    # === Top restaurants by rating with format_card ===
    print("\n=== Top 5 by rating (format_card output) ===")
    for r in top_n(data, n=5):
        print(format_card(r, width=60))
        
    # === Filtering example ===
    print("\n=== Korean restaurants in Koreatown with $$ and rating >= 4.5 (simple print) ===")
    filtered = filter_restaurants(
        data,
        cuisine="Korean",
        neighborhood="Koreatown",
        price="$$",
        min_rating=4.5,
    )
    for r in filtered:
        print(f"- {r['name']} ({r['cuisine']}, {r['price']}) ★ {r['rating']} – {r['sample_dish']}")

    # === Same filter + card display ===
    print("\n=== Same filtered results (format_card output) ===")
    for r in filtered:
        print(format_card(r, width=60))

if __name__ == "__main__":
    main()