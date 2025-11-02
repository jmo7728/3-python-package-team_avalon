from eatnyc import load_data, top_n, filter_restaurants, format_card # add others as they land

def main():
    data = load_data()
    print("rows:", len(data))
    print("Top by rating:")
    for r in top_n(data, n=5):
        print(f"- {r['name']}  ({r['cuisine']}, {r['price']})  ★ {r['rating']}  – {r['sample_dish']}")
        
    print("filtering Korean restaurants in Koreatown with a $$ price and a min_rating of 4.5):")
    for r in filter_restaurants(data, cuisine="Korean", neighborhood="Koreatown", price="$$", min_rating=4.5):
        print(f"- {r['name']}  ({r['cuisine']}, {r['price']})  ★ {r['rating']}  – {r['sample_dish']}")

if __name__ == "__main__":
    main()