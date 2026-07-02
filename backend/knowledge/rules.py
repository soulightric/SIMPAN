RULES = [
    {
        "id": 1,
        "name": "DEFISIT",
        "description": "Pengeluaran melebihi pemasukan",
        "message": "❌ Pengeluaran melebihi pemasukan. Anda mengalami defisit.",
        "condition": lambda d: d["total_pengeluaran"] > d["pemasukan"]
    },

    {
        "id": 2,
        "name": "HIBURAN_BERLEBIHAN",
        "description": "Pengeluaran hiburan lebih dari 20%",
        "message": "🎮 Pengeluaran hiburan melebihi 20% dari pemasukan.",
        "condition": lambda d: d["hiburan"] > d["pemasukan"] * 0.20
    },

    {
        "id": 3,
        "name": "SALDO_RENDAH",
        "description": "Saldo kurang dari 10%",
        "message": "💰 Saldo kurang dari 10% dari pemasukan.",
        "condition": lambda d: d["saldo"] < d["pemasukan"] * 0.10
    },

    {
        "id": 4,
        "name": "KEUANGAN_SEHAT",
        "description": "Saldo lebih dari 30%",
        "message": "✅ Kondisi keuangan sehat.",
        "condition": lambda d: d["saldo"] >= d["pemasukan"] * 0.30
    }
]