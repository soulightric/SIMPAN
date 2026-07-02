from backend.database.db import db
from backend.database.models import History


def save_history(data):

    history = History(

        pemasukan=data["pemasukan"],

        total_pengeluaran=data["total_pengeluaran"],

        saldo=data["saldo"],

        target=data["target"],

        deadline=data["deadline"]

    )

    db.session.add(history)

    db.session.commit()

    return history


def get_all_history():

    history = History.query.order_by(
        History.created_at.desc()
    ).all()

    return history