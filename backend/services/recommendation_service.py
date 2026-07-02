class RecommendationService:

    def generate(self, finance, rules, plan):

        rekomendasi = []

        # Rule-Based
        for rule in rules:
            rekomendasi.append(rule["message"])

        # Planning
        if plan["cukup"]:
            rekomendasi.append(
                f"Sisihkan minimal Rp {plan['target_per_bulan']:,.0f} setiap bulan."
            )
        else:
            rekomendasi.append(
                f"Tambahkan tabungan sekitar Rp {plan['kekurangan']:,.0f} per bulan."
            )

        # Kategori terbesar
        kategori = {
            "Makanan": finance["makanan"],
            "Transportasi": finance["transportasi"],
            "Pendidikan": finance["pendidikan"],
            "Hiburan": finance["hiburan"],
            "Lainnya": finance["lainnya"]
        }

        terbesar = max(kategori, key=kategori.get)

        rekomendasi.append(
            f"Pengeluaran terbesar berada pada kategori {terbesar}."
        )

        return rekomendasi