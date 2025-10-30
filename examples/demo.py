from eatnyc import load_data, top_n  # add others as they land

def main():
    data = load_data()
    print("rows:", len(data))
    print("Top by rating:")
    for r in top_n(data, n=5):
        print(f"- {r['name']}  ({r['cuisine']}, {r['price']})  ★ {r['rating']}  – {r['sample_dish']}")

if __name__ == "__main__":
    main()