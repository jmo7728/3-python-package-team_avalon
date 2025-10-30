import csv
import random
import os
from importlib.resources import files 

_DATA_PKG = "eatnyc.data"
_DEFAULT_CSV = "nyc_restaurant_data.csv"

#columns we expect in the CSV 
_REQUIRED_COLS = {"name", "cuisine","neighborhood", "price", "rating", "sample_dish"}


#new function (NORMALIZE_ROWS)
def _normalize_row(row: dict) -> dict:
    """Clean up one CSV row: strip spaces, normalize case/types, compute helper fields."""
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
    #Adds helper lists: `_cuisines`, `_vibes`.
    
    if path is None:
        # use the packaged resource
        csv_path = files(_DATA_PKG) / _DEFAULT_CSV
        f = csv_path.open("r", encoding="utf-8")
        close_after = True
    else:
        f = open(path, "r", encoding="utf-8")
        close_after = True

    try:
        reader = csv.DictReader(f)
        # validate required headers
        if validate:
            cols = {c.strip().lower() for c in reader.fieldnames or []}
            missing = _REQUIRED_COLS - cols
            if missing:
                raise ValueError(f"CSV missing required columns: {sorted(missing)}")

        data = [_normalize_row(r) for r in reader]
        return data
    finally:
        if close_after:
            f.close()



def filter_restaurants(data, cuisine=None, neighborhood=None, price=None, min_rating=None, vibe=None, limit=None):
    return


def top_n(data, n=5, sort_by="rating", descending=True):
    return


def sample_dish(cuisine=None, seed=None):
    return


def format_card(row, style="ascii", width=48, show_vibes=True):
    return
