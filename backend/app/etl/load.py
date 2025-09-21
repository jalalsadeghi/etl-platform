from app.models.external_user import ExternalUser
from app.models.user import User
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session


def load_users(df, db: Session):
    # ensure columns exist
    email_col = "email"
    name_col = (
        "full_name"
        if "full_name" in df.columns
        else ("name" if "name" in df.columns else None)
    )

    created = 0
    for _, r in df.iterrows():
        email = r.get(email_col)
        if not isinstance(email, str):
            continue
        user = User(email=email, full_name=(r.get(name_col) if name_col else None))
        db.add(user)
        created += 1
    db.commit()
    return created


def upsert_external_users(df, db: Session) -> int:
    if df.empty:
        return 0
    rows = df.to_dict(orient="records")
    stmt = insert(ExternalUser).values(rows)
    # On conflict by ext_id, update name/email
    stmt = stmt.on_conflict_do_update(
        index_elements=[ExternalUser.ext_id],
        set_={
            "name": stmt.excluded.name,
            "email": stmt.excluded.email,
        },
    )
    result = db.execute(stmt)
    db.commit()
    return result.rowcount or 0
