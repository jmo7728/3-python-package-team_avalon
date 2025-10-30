from eatnyc import load_data, filter_restaurants, top_n, sample_dish

def test_load_data_has_rows():
    data = load_data()
    assert isinstance(data, list)
    assert len(data) >= 1
    # basic schema check
    for key in ["name", "cuisine", "neighborhood", "price", "rating", "sample_dish"]:
        assert key in data[0]