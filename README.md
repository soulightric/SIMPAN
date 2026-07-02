# 💰 SIMPAN — Smart Budget Planner

**SIMPAN** adalah aplikasi web perencana keuangan pribadi berbasis **Knowledge-Based AI**.
Pengguna memasukkan pemasukan, pengeluaran per kategori, serta target tabungan, lalu aplikasi
menganalisis kondisi keuangan menggunakan *rule engine*, membuat rencana tabungan, dan memberi
rekomendasi — semuanya divisualisasikan dalam dashboard yang responsif.

> Dibangun dengan **Flask + SQLite** di backend dan **Vanilla JS + Bootstrap 5 + Chart.js** di frontend.

---

## 📑 Daftar Isi
- [Fitur](#-fitur)
- [Tech Stack](#-tech-stack)
- [Struktur Proyek](#-struktur-proyek)
- [Instalasi & Menjalankan](#-instalasi--menjalankan)
- [Cara Kerja AI (Knowledge-Based)](#-cara-kerja-ai-knowledge-based)
- [Referensi API](#-referensi-api)
- [Frontend](#-frontend)
- [Responsivitas](#-responsivitas)
- [Testing](#-testing)
- [Catatan Pengembangan](#-catatan-pengembangan)

---

## ✨ Fitur

- **Analisis keuangan otomatis** — hitung total pengeluaran & saldo secara instan.
- **Knowledge-Based Rule Engine** — deteksi defisit, saldo rendah, hiburan berlebihan, dan kondisi sehat.
- **Perencanaan tabungan** — hitung target menabung per bulan & kekurangannya terhadap deadline.
- **Rekomendasi cerdas** — saran berbasis aturan, rencana, dan kategori pengeluaran terbesar.
- **Financial Health Score** — skor 0–100 dinamis dengan label *Sangat Baik / Baik / Waspada / Kritis*.
- **Visualisasi** — pie chart distribusi pengeluaran & bar chart income vs expense.
- **Riwayat analisis** — tersimpan di database, dengan pencarian & ekspor CSV.
- **UI responsif** — bekerja mulus di desktop, tablet, dan ponsel (sidebar drawer + backdrop).

---

## 🛠 Tech Stack

| Lapisan | Teknologi |
|---|---|
| Backend | Python 3, Flask, Flask-SQLAlchemy, Flask-Cors |
| Database | SQLite (`backend/database/simpan.db`) |
| Frontend | HTML (Jinja2), Bootstrap 5.3, Bootstrap Icons, Chart.js 4, Vanilla JavaScript |
| Testing | pytest |

---

## 📂 Struktur Proyek

```
SIMPAN/
├── app.py                      # Entry point — membuat & menjalankan Flask app
├── requirements.txt            # Dependensi Python
├── backend/
│   ├── __init__.py             # create_app(): app factory, registrasi blueprint & DB
│   ├── config.py               # Konfigurasi (SECRET_KEY, URI database)
│   ├── routes.py               # Semua route web & REST API
│   ├── database/
│   │   ├── db.py               # Instance SQLAlchemy
│   │   ├── models.py           # Model History
│   │   └── simpan.db           # File database SQLite
│   ├── knowledge/
│   │   └── rules.py            # Basis pengetahuan (daftar aturan/RULES)
│   └── services/
│       ├── ai_service.py       # Orkestrator: gabungkan finance + rules + planning + rekomendasi
│       ├── finance_service.py  # Hitung total pengeluaran & saldo
│       ├── rule_engine.py      # Evaluasi aturan terhadap kondisi keuangan
│       ├── planning_service.py # Hitung rencana tabungan
│       ├── recommendation_service.py  # Susun daftar rekomendasi
│       └── history_service.py  # Simpan & ambil riwayat
├── frontend/
│   ├── templates/
│   │   ├── layouts/app.html    # Layout dasar (navbar, sidebar, footer, script)
│   │   ├── components/         # navbar.html, sidebar.html
│   │   ├── dashboard.html      # Halaman utama
│   │   └── history.html        # Halaman riwayat
│   └── static/
│       ├── css/                # variable.css, base.css, style.css
│       ├── js/                 # api, app, chart, dashboard, history, sidebar, toast, loading
│       └── favicon.ico
└── tests/
    ├── test_rule.py            # Unit test rule engine
    └── test_planning.py        # Unit test planning service
```

---

## 🚀 Instalasi & Menjalankan

**Prasyarat:** Python 3.9+.

```bash
# 1. (opsional) buat virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. install dependensi
pip install -r requirements.txt

# 3. jalankan aplikasi
python app.py
```

Aplikasi berjalan di **http://127.0.0.1:5000**.
Database SQLite (`simpan.db`) dibuat otomatis saat pertama kali dijalankan.

---

## 🧠 Cara Kerja AI (Knowledge-Based)

Alur analisis (`POST /api/analyze`) dijalankan oleh `AIService.analyze()`:

```
input → finance_service → rule_engine → planning_service → recommendation_service → output
```

### 1. Perhitungan Keuangan (`finance_service.py`)
```
total_pengeluaran = makanan + transportasi + pendidikan + hiburan + lainnya
saldo             = pemasukan − total_pengeluaran
```

### 2. Rule Engine (`knowledge/rules.py`)
Setiap aturan berupa kondisi (lambda) yang dievaluasi terhadap data keuangan:

| ID | Nama | Kondisi | Pesan |
|----|------|---------|-------|
| 1 | `DEFISIT` | `total_pengeluaran > pemasukan` | ❌ Pengeluaran melebihi pemasukan |
| 2 | `HIBURAN_BERLEBIHAN` | `hiburan > 20% pemasukan` | 🎮 Hiburan melebihi 20% |
| 3 | `SALDO_RENDAH` | `saldo < 10% pemasukan` | 💰 Saldo kurang dari 10% |
| 4 | `KEUANGAN_SEHAT` | `saldo ≥ 30% pemasukan` | ✅ Kondisi keuangan sehat |

> Menambah aturan baru cukup dengan menambahkan satu objek `{id, name, description, message, condition}` ke list `RULES`.

### 3. Planning (`planning_service.py`)
```
target_per_bulan = target / deadline        # deadline minimal 1 bulan
cukup            = saldo ≥ target_per_bulan
kekurangan       = max(0, target_per_bulan − saldo)
```

### 4. Rekomendasi (`recommendation_service.py`)
Menggabungkan: pesan dari aturan yang aktif + saran menabung dari rencana + kategori pengeluaran terbesar.

### 5. Financial Health Score (frontend — `app.js`)
Skor mulai dari 100 dan dikurangi berdasarkan kondisi:

| Kondisi | Pengurangan |
|---------|-------------|
| Defisit (`pengeluaran > pemasukan`) | −40 |
| Saldo < 10% pemasukan | −20 |
| Hiburan > 20% pemasukan | −10 |
| Target belum aman (`cukup = false`) | −15 |

Label: **≥80** Sangat Baik · **≥60** Baik · **≥40** Waspada · **<40** Kritis.

---

## 🔌 Referensi API

Base URL: `http://127.0.0.1:5000`

### Halaman (HTML)
| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/` | Dashboard |
| `GET` | `/history` | Halaman riwayat |

### REST API (JSON)

#### `POST /api/analyze`
Menganalisis data keuangan dan menyimpannya ke riwayat.

**Request body:**
```json
{
  "pemasukan": 10000000,
  "makanan": 3000000,
  "transportasi": 1000000,
  "pendidikan": 500000,
  "hiburan": 2500000,
  "lainnya": 500000,
  "target": 12000000,
  "deadline": 6
}
```

**Response `200`:**
```json
{
  "finance":  { "pemasukan": 10000000, "total_pengeluaran": 7500000, "saldo": 2500000, "...": "..." },
  "rules":    [ { "rule_id": 2, "rule": "HIBURAN_BERLEBIHAN", "message": "🎮 ..." } ],
  "planning": { "target_per_bulan": 2000000, "cukup": true, "kekurangan": 0, "...": "..." },
  "recommendation": [ "🎮 ...", "Sisihkan minimal Rp 2.000.000 ...", "Pengeluaran terbesar ... Makanan." ]
}
```

#### `GET /api/history`
Mengembalikan daftar riwayat (terbaru dulu).
```json
[
  { "id": 1, "pemasukan": 10000000, "total_pengeluaran": 7500000,
    "saldo": 2500000, "target": 12000000, "deadline": 6, "created_at": "2026-07-02 14:32" }
]
```

#### `POST /api/history`
Menyimpan satu entri riwayat secara manual. Body: `pemasukan, total_pengeluaran, saldo, target, deadline`. → `201`

#### `DELETE /api/history/<id>`
Menghapus entri riwayat berdasarkan ID.
- `200` → `{ "message": "Berhasil dihapus" }`
- `404` → `{ "message": "Data tidak ditemukan" }`

---

## 🎨 Frontend

| File JS | Tanggung jawab |
|---------|----------------|
| `api.js` | Wrapper `fetch` untuk semua endpoint API |
| `app.js` | Handler form, update dashboard, health score, status & planning |
| `chart.js` | Menggambar pie & bar chart (Chart.js) |
| `dashboard.js` | Jam & salam real-time |
| `history.js` | Muat riwayat, pencarian, ekspor CSV, hapus |
| `sidebar.js` | Toggle sidebar, drawer mobile + backdrop, menu aktif, ingat collapse |
| `toast.js` | Notifikasi toast (Bootstrap) |
| `loading.js` | Overlay loading saat analisis |

**CSS** dimuat berurutan: `variable.css` (variabel warna/spacing) → `base.css` (reset) → `style.css` (komponen & responsif).

---

## 📱 Responsivitas

- **Desktop (>992px):** sidebar tetap; bisa di-*collapse* (status diingat via `localStorage`).
- **Tablet/Ponsel (≤992px):** sidebar menjadi *drawer* off-canvas dengan **backdrop**; tertutup saat klik backdrop, tekan `Esc`, atau memilih menu.
- **Breakpoint:** grid ringkasan menyusut 4 → 2 → 1 kolom; navbar & welcome card menyesuaikan.
- Grid menggunakan `minmax(0, 1fr)` dan chart dibungkus container tinggi tetap agar **tidak ada overflow horizontal** di ukuran layar mana pun.

---

## 🧪 Testing

```bash
pip install pytest
pytest -q
```

Cakupan test:
- `tests/test_rule.py` — kondisi sehat, defisit, dan hiburan berlebihan.
- `tests/test_planning.py` — rencana cukup/kurang & penanganan `deadline = 0` (anti divide-by-zero).

---

## 📝 Catatan Pengembangan

- **App factory pattern** (`create_app`) memudahkan testing & konfigurasi.
- Basis pengetahuan (`RULES`) sengaja dipisah dari mesinnya (`RuleEngine`) agar mudah diperluas tanpa mengubah logika.
- Untuk mereset data, hapus file `backend/database/simpan.db` — akan dibuat ulang otomatis.
- Mode debug aktif secara default (`app.run(debug=True)`); matikan untuk produksi.

---

© 2026 SIMPAN — Smart Budget Planner