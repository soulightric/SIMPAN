from flask import Blueprint
from flask import jsonify
from flask import request
from flask import render_template
from backend.services.ai_service import AIService
from backend.database.db import db
from backend.database.models import History

from backend.services.history_service import (
    save_history,
    get_all_history
)

ai = AIService()

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")

@main.route("/history")
def history_page():
    return render_template("history.html")


@main.route("/api/history", methods=["GET"])
def history():

    data = get_all_history()

    return jsonify(

        [

            item.to_dict()

            for item in data

        ]

    )


@main.route("/api/history", methods=["POST"])
def create_history():

    body = request.json

    history = save_history(body)

    return jsonify(history.to_dict()), 201


@main.route("/api/analyze", methods=["POST"])
def analyze():

    body = request.get_json()

    result = ai.analyze(body)

    save_history({
        "pemasukan": result["finance"]["pemasukan"],
        "total_pengeluaran": result["finance"]["total_pengeluaran"],
        "saldo": result["finance"]["saldo"],
        "target": result["finance"]["target"],
        "deadline": result["finance"]["deadline"]
    })

    return jsonify(result)

@main.route("/api/history/<int:id>", methods=["DELETE"])
def delete_history(id):

    history = History.query.get(id)

    if not history:
        return jsonify({
            "message": "Data tidak ditemukan"
        }), 404

    db.session.delete(history)
    db.session.commit()

    return jsonify({
        "message": "Berhasil dihapus"
    })