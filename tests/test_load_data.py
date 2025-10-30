from eatnyc import load_data

def test_load_data_has_rows():
    data = load_data()
    assert isinstance(data, list)
    assert len(data) >= 1
    # basic schema check
    for key in ["name", "cuisine", "neighborhood", "price", "rating", "sample_dish"]:
        assert key in data[0]

def test_load_data_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_data(path="does_not_exist.csv")

def test_load_data_has_required_columns():
    data = load_data()
    for key in ["name","cuisine","neighborhood","price","rating","sample_dish"]:
        assert key in data[0]