def generate_recommendation(data, hasil, plan, rules):

    rekomendasi = []

    # Tambahkan hasil Rule-Based
    rekomendasi.extend(rules)

    # Tambahkan hasil Planning
    if plan["cukup"]:
        rekomendasi.append(
            f"✅ Sisihkan minimal Rp {plan['tabungan_per_bulan']:,.0f} setiap bulan agar target tercapai."
        )
    else:
        rekomendasi.append(
            f"⚠ Anda perlu menambah tabungan sebesar Rp {plan['kekurangan']:,.0f} setiap bulan."
        )

    # Rekomendasi berdasarkan kategori terbesar
    kategori = {
        "Makanan": data["makanan"],
        "Transportasi": data["transportasi"],
        "Pendidikan": data["pendidikan"],
        "Hiburan": data["hiburan"],
        "Lainnya": data["lainnya"]
    }

    terbesar = max(kategori, key=kategori.get)

    rekomendasi.append(
        f"📊 Pengeluaran terbesar berada pada kategori {terbesar}. Pertimbangkan untuk mengoptimalkan pengeluaran pada kategori tersebut."
    )

    # Saldo positif
    if hasil["saldo"] > 0:
        rekomendasi.append(
            "💡 Sisihkan tabungan segera setelah menerima pemasukan (Pay Yourself First)."
        )

    return rekomendasi