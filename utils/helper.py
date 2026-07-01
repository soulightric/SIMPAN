def hitung_keuangan(data):
    total_pengeluaran = (
        data["makanan"]
        + data["transportasi"]
        + data["pendidikan"]
        + data["hiburan"]
        + data["lainnya"]
    )

    saldo = data["pemasukan"] - total_pengeluaran

    return {
        "total_pengeluaran": total_pengeluaran,
        "saldo": saldo
    }