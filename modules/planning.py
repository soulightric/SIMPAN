def create_plan(data, hasil):

    target = data["target_tabungan"]
    deadline = data["deadline"]
    saldo = hasil["saldo"]

    # Menghindari pembagian dengan nol
    if deadline <= 0:
        deadline = 1

    tabungan_per_bulan = target / deadline

    cukup = saldo >= tabungan_per_bulan

    kekurangan = 0

    if not cukup:
        kekurangan = tabungan_per_bulan - saldo

    return {
        "tabungan_per_bulan": tabungan_per_bulan,
        "cukup": cukup,
        "kekurangan": kekurangan
    }