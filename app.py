import streamlit as st
from modules.input_data import input_keuangan
from utils.helper import hitung_keuangan
from modules.rule_engine import check_rules
from modules.planning import create_plan
from modules.recommendation import generate_recommendation
from modules.database import simpan_data
from modules.database import load_data
from utils.financial_health import financial_health
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="SIMPAN",
    page_icon="💰",
    layout="wide"
)

st.sidebar.title("💰 SIMPAN")

st.sidebar.info("""
Smart Budget Planner

Knowledge-Based AI
- Rule-Based Reasoning
- Planning
""")

st.sidebar.success("Versi 1.0")


st.title("💰 Smart Budget Planner (SIMPAN)")
st.write("Kelola keuanganmu dengan lebih cerdas.")

data = input_keuangan()

if data["pemasukan"] <= 0:
    st.error("Pemasukan harus lebih dari Rp0.")
    st.stop()

if data["target_tabungan"] <= 0:
    st.error("Target tabungan harus lebih dari Rp0.")
    st.stop()

if data["deadline"] <= 0:
    st.error("Deadline minimal 1 bulan.")
    st.stop()


# Tombol analisis
if st.button("🔍 Analisis Keuangan"):

    hasil = hitung_keuangan(data)
    status, pesan = financial_health(data, hasil)
    rekomendasi = check_rules(data, hasil)
    plan = create_plan(data, hasil)
    simpan_data(data, hasil, plan)
    final_rekomendasi = generate_recommendation(
        data,
        hasil,
        plan,
        rekomendasi
    )

    chart = pd.DataFrame(
        {
            "Nominal": [
                data["makanan"],
                data["transportasi"],
                data["pendidikan"],
                data["hiburan"],
                data["lainnya"]
            ]
        },
        index=[
            "Makanan",
            "Transportasi",
            "Pendidikan",
            "Hiburan",
            "Lainnya"
        ]
    )
    
    st.subheader("🥧 Persentase Pengeluaran")

    labels = [
        "Makanan",
        "Transportasi",
        "Pendidikan",
        "Hiburan",
        "Lainnya"
    ]

    sizes = [
        data["makanan"],
        data["transportasi"],
        data["pendidikan"],
        data["hiburan"],
        data["lainnya"]
    ]

    # Hilangkan kategori dengan nilai 0
    filtered_labels = []
    filtered_sizes = []

    for label, size in zip(labels, sizes):
        if size > 0:
            filtered_labels.append(label)
            filtered_sizes.append(size)

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.pie(
        filtered_sizes,
        labels=filtered_labels,
        autopct='%1.1f%%',
        startangle=90
    )

    ax.axis("equal")  # Membuat pie chart berbentuk lingkaran sempurna

    st.pyplot(fig)

    compare = pd.DataFrame(
        {
            "Nominal": [
                data["pemasukan"],
                hasil["total_pengeluaran"]
            ]
        },
        index=[
            "Pemasukan",
            "Pengeluaran"
        ]
    )

    st.subheader("💵 Pemasukan vs Pengeluaran")

    st.bar_chart(compare)

    persen = 0

    if data["target_tabungan"] > 0:
        persen = min(
            hasil["saldo"] / data["target_tabungan"],
            1.0
        )

    st.subheader("🎯 Progress Target Tabungan")

    st.progress(persen)

    st.write(
        f"{persen*100:.1f}% dari target tabungan dapat dipenuhi dengan saldo saat ini."
    )


    st.divider()

    st.subheader("📊 Ringkasan Keuangan")

    st.divider()

    st.subheader("🤖 Analisis AI (Rule-Based Reasoning)")

    if rekomendasi:

        for item in rekomendasi:
            st.info(item)

    else:
        st.success("Tidak ditemukan masalah pada kondisi keuangan.")

    st.subheader("🚦 Status Keuangan")

    st.metric(
        "Kondisi",
        status
    )

    st.write(pesan)

    st.divider()

    st.subheader("🎯 Rencana Tabungan")

    st.metric(
        "Target Tabungan per Bulan",
        f"Rp {plan['tabungan_per_bulan']:,.0f}"
    )

    if plan["cukup"]:

        st.success(
            "Saldo saat ini mencukupi untuk mencapai target tabungan."
        )

    else:

        st.error(
            f"Saldo belum mencukupi. Anda perlu menghemat sekitar Rp {plan['kekurangan']:,.0f} setiap bulan."
        )

    st.divider()

    st.subheader("🧠 Rekomendasi Keuangan SIMPAN")

    for item in final_rekomendasi:
        st.success(item)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Pemasukan",
        f"Rp {data['pemasukan']:,.0f}"
    )

    col2.metric(
        "Total Pengeluaran",
        f"Rp {hasil['total_pengeluaran']:,.0f}"
    )

    col3.metric(
        "Saldo",
        f"Rp {hasil['saldo']:,.0f}"
    )

    st.divider()

    st.subheader("📋 Detail Pengeluaran")

    st.table({
        "Kategori": [
            "Makanan",
            "Transportasi",
            "Pendidikan",
            "Hiburan",
            "Lainnya"
        ],
        "Nominal": [
            data["makanan"],
            data["transportasi"],
            data["pendidikan"],
            data["hiburan"],
            data["lainnya"]
        ]
    })

    st.divider()

    st.subheader("📁 Riwayat Analisis")

    history = load_data()

    if history.empty:

        st.info("Belum ada data.")

    else:

        st.dataframe(
            history,
            use_container_width=True
        )

    history = load_data()

    if not history.empty:
        csv = history.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Riwayat",
            data=csv,
            file_name="riwayat_analisis.csv",
            mime="text/csv"
        )

    st.subheader("📌 Kesimpulan")

    if hasil["saldo"] > 0:
        st.success(
            f"Anda masih memiliki saldo sebesar Rp {hasil['saldo']:,.0f}."
        )
    else:
        st.error(
            "Pengeluaran telah melebihi pemasukan."
        )

    st.write(
        f"Target tabungan sebesar Rp {data['target_tabungan']:,.0f} "
        f"dalam {data['deadline']} bulan."
    )