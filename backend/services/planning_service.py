class PlanningService:

    def create_plan(self, finance):

        target = finance["target"]
        deadline = finance["deadline"]
        saldo = finance["saldo"]

        if deadline <= 0:
            deadline = 1

        target_per_bulan = target / deadline

        cukup = saldo >= target_per_bulan

        kekurangan = 0

        if not cukup:
            kekurangan = target_per_bulan - saldo

        return {
            "target_tabungan": target,
            "deadline": deadline,
            "target_per_bulan": target_per_bulan,
            "saldo_saat_ini": saldo,
            "cukup": cukup,
            "kekurangan": max(0, kekurangan)
        }