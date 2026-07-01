import streamlit as st


def input_keuangan():
    st.header("📥 Input Data Keuangan")

    pemasukan = st.number_input(
        "Pemasukan Bulanan (Rp)",
        min_value=0,
        step=50000
    )

    makanan = st.number_input(
        "Pengeluaran Makanan (Rp)",
        min_value=0,
        step=10000
    )

    transportasi = st.number_input(
        "Pengeluaran Transportasi (Rp)",
        min_value=0,
        step=10000
    )

    pendidikan = st.number_input(
        "Pengeluaran Pendidikan (Rp)",
        min_value=0,
        step=10000
    )

    hiburan = st.number_input(
        "Pengeluaran Hiburan (Rp)",
        min_value=0,
        step=10000
    )

    lainnya = st.number_input(
        "Pengeluaran Lainnya (Rp)",
        min_value=0,
        step=10000
    )

    target_tabungan = st.number_input(
        "Target Tabungan (Rp)",
        min_value=0,
        step=50000
    )

    deadline = st.number_input(
        "Target Tercapai Dalam (Bulan)",
        min_value=1,
        step=1
    )

    return {
        "pemasukan": pemasukan,
        "makanan": makanan,
        "transportasi": transportasi,
        "pendidikan": pendidikan,
        "hiburan": hiburan,
        "lainnya": lainnya,
        "target_tabungan": target_tabungan,
        "deadline": deadline
    }