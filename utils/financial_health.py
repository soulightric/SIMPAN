def financial_health(data, hasil):

    pemasukan = data["pemasukan"]
    pengeluaran = hasil["total_pengeluaran"]

    rasio = pengeluaran / pemasukan if pemasukan > 0 else 0

    if rasio <= 0.70:
        return "🟢 Baik", "Keuangan dalam kondisi sehat."

    elif rasio <= 0.90:
        return "🟡 Waspada", "Pengeluaran mulai mendekati pemasukan."

    else:
        return "🔴 Defisit", "Pengeluaran terlalu tinggi."