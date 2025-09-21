from app.etl.transform import to_users_df


def test_transform_users_demo():
    rows = [
        {"id": 1, "name": "A", "email": "a@x.com"},
        {"id": 1, "name": "A", "email": "a@x.com"},
    ]
    df = to_users_df(rows)
    assert len(df) == 1
    assert set(df.columns) == {"ext_id", "name", "email"}
