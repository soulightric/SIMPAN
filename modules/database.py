import pandas as pd
import os

FILE_NAME = "data/transaksi.csv"


def simpan_data(data, hasil, plan):
    """
    Menyimpan hasil analisis ke file CSV.
    """

    row = {
        "Pemasukan": data["pemasukan"],
        "Makanan": data["makanan"],
        "Transportasi": data["transportasi"],
        "Pendidikan": data["pendidikan"],
        "Hiburan": data["hiburan"],
        "Lainnya": data["lainnya"],
        "Total Pengeluaran": hasil["total_pengeluaran"],
        "Saldo": hasil["saldo"],
        "Target": data["target_tabungan"],
        "Deadline": data["deadline"],
        "Target/Bulan": plan["tabungan_per_bulan"]
    }

    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
    else:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    df.to_csv(FILE_NAME, index=False)

def load_data():

    if os.path.exists(FILE_NAME):

        return pd.read_csv(FILE_NAME)

    return pd.DataFrame()