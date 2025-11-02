import csv
import random
import os
from importlib.resources import files 

_DATA_PKG = "eatnyc"
_DEFAULT_CSV = "data/nyc_restaurant_data.csv"

#columns we expect in the CSV 
_REQUIRED_COLS = {"name", "cuisine","neighborhood", "price", "rating", "sample_dish"}


#new function (NORMALIZE_ROWS)
def _normalize_row(row: dict) -> dict:
    #Clean up one CSV row: strip spaces, normalize case/types, compute helper fields.
    clean = {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}

    # rating → float (default 0.0)
    try:
        clean["rating"] = float(clean.get("rating", "") or 0.0)
    except ValueError:
        clean["rating"] = 0.0

    # cuisines list (split on / , ; | )
    raw_c = clean.get("cuisine", "")
    parts = []
    for sep in ["/", ",", ";", "|"]:
        raw_c = raw_c.replace(sep, " ")
    parts = [p for p in (w.strip().lower() for w in raw_c.split()) if p]
    clean["_cuisines"] = parts  # helper list for filtering

    # price normalize (e.g., $, $$, $$$)
    clean["price"] = (clean.get("price") or "").strip()

    return clean

#Load the NYC restaurant CSV into a list of dicts.
def load_data(path: str | None = None, validate: bool = True) -> list[dict]:

    #If `path` is None, loads the bundled file from eatnyc/data/.
    #Keys are lowercased; rating is converted to float.
    #Adds helper lists: `_cuisines`.
    if path is None:
        #use importlib.resources so this works from wheels/zip installs
        resource = files(_DATA_PKG) / _DEFAULT_CSV
        f = resource.open("r", encoding="utf-8", newline="")
    else:
        f = open(path, "r", encoding="utf-8", newline="")

    with f as fh:
        reader = csv.DictReader(fh)

        if validate:
            cols = {c.strip().lower() for c in (reader.fieldnames or [])}
            missing = _REQUIRED_COLS - cols
            if missing:
                raise ValueError(f"CSV missing required columns: {sorted(missing)}")

        return [_normalize_row(r) for r in reader]


def filter_restaurants(data, cuisine=None, neighborhood=None, price=None, min_rating=None, vibe=None, limit=None):
    if not isinstance(data, list):
        raise TypeError("Data must be a list of dicts")
    
    if not data:
        return []
    
    results = []
    for row in data:
        if cuisine:
            if cuisine.strip().lower() not in row.get("cuisines", []):
                continue

        if neighborhood:
            if neighborhood.strip().lower() != row.get("neighborhood", "").lower():
                continue

        if price:
            if price.strip() != row.get("price", ""):
                continue

        if min_rating:
            try:
                min_rating_val = float(min_rating)
            except ValueError:
                raise ValueError("min_rating must be a number")
            if row.get("rating", 0.0) < min_rating_val:
                continue

        results.append(row)

        if limit:
            if len(results) >= limit:
                break
    return results


def top_n(data, n=5, sort_by="rating", descending=True):
    if not isinstance(data, list):
        raise TypeError("data must be a list of dicts")

    if not data:
        return []

    # normalize sort key to lower-case to match load_data normalization
    sort_key = (sort_by or "").strip().lower()
    if not sort_key:
        raise ValueError("sort_by must be a non-empty string")

    # validate the key exists in at least one row; otherwise error for clarity
    if all((sort_key not in row) for row in data if isinstance(row, dict)):
        raise KeyError(f"sort_by key not found in data rows: '{sort_key}'")

    def key_func(row):
        # Missing keys sort as None -> treated as smallest when descending=False, largest when descending=True
        value = row.get(sort_key)
        # Ensure consistent comparison for mixed types
        if isinstance(value, (int, float)):
            return value
        return ("" if value is None else str(value).lower())

    try:
        sorted_rows = sorted(
            (r for r in data if isinstance(r, dict)),
            key=key_func,
            reverse=bool(descending),
        )
    except TypeError:
        # Fallback: convert all keys to string for sorting if mixed incomparable types
        sorted_rows = sorted(
            (r for r in data if isinstance(r, dict)),
            key=lambda r: str(r.get(sort_key, "")),
            reverse=bool(descending),
        )

    if n is None:
        return sorted_rows
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer or None")
    return sorted_rows[:n]


def sample_dish(cuisine=None, seed=None):
    return


def format_card(row, style="ascii", width=48, show_vibes=True):
    return


def cli(argv=None):
    import argparse
    # Simple command-line entrypoint:
    #   $ eatnyc            -> prints top 5 by rating
    #   $ eatnyc -n 10      -> prints top 10
    #   $ eatnyc --sort name --asc -> sort by name ascending
    
    parser = argparse.ArgumentParser(prog="eatnyc", description="NYC restaurant recommender")
    parser.add_argument("-n", "--n", type=int, default=5, help="number of results")
    parser.add_argument("--sort", default="rating", help="field to sort by (rating, name, price, etc.)")
    parser.add_argument("--asc", action="store_true", help="sort ascending (default is descending)")
    args = parser.parse_args(argv)

    data = load_data()
    results = top_n(data, n=args.n, sort_by=args.sort, descending=not args.asc)
    for r in results:
        print(f"{r['name']} | {r['cuisine']} | {r['price']} | ★{r['rating']} | {r.get('sample_dish','')}")
