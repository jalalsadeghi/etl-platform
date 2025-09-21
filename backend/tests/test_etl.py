from app.etl.transform import clean_rows


def test_clean_rows_basic():
    rows = [
        {"id": 1, "name": "A", "email": "a@x.com"},
        {"id": 1, "name": "A", "email": "a@x.com"},
    ]
    df = clean_rows(rows)
    assert len(df) == 1
