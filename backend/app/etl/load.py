from app.models.user import User
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
