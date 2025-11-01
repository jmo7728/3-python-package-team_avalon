from eatnyc import load_data, top_n, format_card  # add others as they land

def main():
    data = load_data()
    print("rows:", len(data))
    print("Top by rating:")
    for r in top_n(data, n=5):
        print(format_card(r, width=60))

if __name__ == "__main__":
    main()