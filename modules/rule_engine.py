def check_rules(data, hasil):

    rekomendasi = []

    pemasukan = data["pemasukan"]
    pengeluaran = hasil["total_pengeluaran"]
    saldo = hasil["saldo"]

    # Rule 1
    if pengeluaran > pemasukan:
        rekomendasi.append(
            "❌ Pengeluaran melebihi pemasukan. Anda mengalami defisit."
        )

    # Rule 2
    if data["hiburan"] > pemasukan * 0.20:
        rekomendasi.append(
            "🎮 Pengeluaran hiburan melebihi 20% dari pemasukan. Kurangi biaya hiburan."
        )

    # Rule 3
    if saldo < pemasukan * 0.10:
        rekomendasi.append(
            "💰 Saldo kurang dari 10% pemasukan. Tingkatkan alokasi tabungan."
        )

    # Rule 4
    if saldo > pemasukan * 0.30:
        rekomendasi.append(
            "✅ Kondisi keuangan cukup baik. Pertahankan pola pengeluaran."
        )

    return rekomendasi