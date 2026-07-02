const form = document.getElementById("financeForm");

if (form) {
    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const data = {
            pemasukan: Number(document.getElementById("pemasukan").value) || 0,
            makanan: Number(document.getElementById("makanan").value) || 0,
            transportasi: Number(document.getElementById("transportasi").value) || 0,
            pendidikan: Number(document.getElementById("pendidikan").value) || 0,
            hiburan: Number(document.getElementById("hiburan").value) || 0,
            lainnya: Number(document.getElementById("lainnya").value) || 0,
            target: Number(document.getElementById("target").value) || 0,
            deadline: Number(document.getElementById("deadline").value) || 0
        };

        try {
            showLoading();
            const result = await API.analyze(data);
            updateDashboard(result);
            showToast("Analisis berhasil.");
        } catch (err) {
            showToast("Gagal melakukan analisis. Coba lagi.");
        } finally {
            hideLoading();
        }
    });
}

function rupiah(value) {
    return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        maximumFractionDigits: 0
    }).format(value || 0);
}

function updateDashboard(result) {

    document.getElementById("incomeValue").innerHTML =
        rupiah(result.finance.pemasukan);

    document.getElementById("expenseValue").innerHTML =
        rupiah(result.finance.total_pengeluaran);

    document.getElementById("balanceValue").innerHTML =
        rupiah(result.finance.saldo);

    const targetValue = document.getElementById("targetValue");
    if (targetValue) {
        targetValue.innerHTML = rupiah(result.finance.target);
    }

    renderRules(result.rules);

    renderRecommendation(result.recommendation);

    drawPieChart(result.finance);

    drawBarChart(result.finance);

    updateProgress(result.finance, result.planning);

    updateFinancialStatus(result.finance);

    updatePlanning(result.planning);

    updateHealthScore(result.finance, result.planning);
}

function updateHealthScore(finance, plan) {

    const scoreEl = document.getElementById("healthScore");
    const statusEl = document.getElementById("healthStatus");
    if (!scoreEl || !statusEl) return;

    let score = 100;
    const income = finance.pemasukan || 0;

    if (finance.total_pengeluaran > income) score -= 40;      // defisit
    if (income && finance.saldo < income * 0.10) score -= 20;  // saldo tipis
    if (income && finance.hiburan > income * 0.20) score -= 10; // hiburan boros
    if (plan && !plan.cukup) score -= 15;                       // target belum aman

    score = Math.max(0, Math.min(100, score));
    scoreEl.innerHTML = score;

    let label, cls;
    if (score >= 80) { label = "Sangat Baik"; cls = "hs-good"; }
    else if (score >= 60) { label = "Baik"; cls = "hs-ok"; }
    else if (score >= 40) { label = "Waspada"; cls = "hs-warn"; }
    else { label = "Kritis"; cls = "hs-bad"; }

    statusEl.innerHTML = label;
    statusEl.className = "health-status " + cls;
}

function renderRules(rules) {

    const list = document.getElementById("ruleList");
    list.innerHTML = "";

    if (!rules || rules.length === 0) {
        list.innerHTML = "<li>Tidak ada peringatan.</li>";
        return;
    }

    rules.forEach(rule => {
        list.innerHTML += `<li>${rule.message}</li>`;
    });
}

function renderRecommendation(data) {

    const list = document.getElementById("recommendationList");
    list.innerHTML = "";

    (data || []).forEach(item => {
        list.innerHTML += `<li>${item}</li>`;
    });
}

function updateFinancialStatus(finance) {

    const status = document.getElementById("financialStatus");
    const message = document.getElementById("financialMessage");

    if (!status || !message) {
        return;
    }

    const ratio = finance.pemasukan
        ? finance.total_pengeluaran / finance.pemasukan
        : 1;

    if (ratio <= 0.7) {
        status.innerHTML = `<span class="badge bg-success">Baik</span>`;
        message.innerHTML = "Keuangan Anda sehat.";
    } else if (ratio <= 0.9) {
        status.innerHTML = `<span class="badge bg-warning">Waspada</span>`;
        message.innerHTML = "Pengeluaran mulai tinggi.";
    } else {
        status.innerHTML = `<span class="badge bg-danger">Defisit</span>`;
        message.innerHTML = "Segera kurangi pengeluaran.";
    }
}

function updatePlanning(plan) {

    const monthlyTarget = document.getElementById("monthlyTarget");
    const planningGap = document.getElementById("planningGap");
    const planningStatus = document.getElementById("planningStatus");

    if (monthlyTarget) {
        monthlyTarget.innerHTML = rupiah(plan.target_per_bulan);
    }
    if (planningGap) {
        planningGap.innerHTML = rupiah(plan.kekurangan);
    }
    if (planningStatus) {
        planningStatus.innerHTML = plan.cukup ? "✅ Tercapai" : "⚠ Belum";
    }
}
