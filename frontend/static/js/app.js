const form = document.getElementById("financeForm");

form.addEventListener("submit", async function(e){

    e.preventDefault();

    const data = {

        pemasukan:Number(document.getElementById("pemasukan").value),

        makanan:Number(document.getElementById("makanan").value),

        transportasi:Number(document.getElementById("transportasi").value),

        pendidikan:Number(document.getElementById("pendidikan").value),

        hiburan:Number(document.getElementById("hiburan").value),

        lainnya:Number(document.getElementById("lainnya").value),

        target:Number(document.getElementById("target").value),

        deadline:Number(document.getElementById("deadline").value)

    };

    try{
        document.getElementById("loadingSpinner").classList.remove("d-none");

        const result = await API.analyze(data);

        updateDashboard(result);

    }

    catch(err){

        alert(err.message);

    }

});

function rupiah(value){

    return new Intl.NumberFormat("id-ID",{

        style:"currency",

        currency:"IDR",

        maximumFractionDigits:0

    }).format(value);

}

function updateDashboard(result){

    document.getElementById("loadingSpinner").classList.add("d-none");

    document.getElementById("incomeValue").innerHTML =
        rupiah(result.finance.pemasukan);

    document.getElementById("expenseValue").innerHTML =
        rupiah(result.finance.total_pengeluaran);

    document.getElementById("balanceValue").innerHTML =
        rupiah(result.finance.saldo);

    renderRules(result.rules);

    renderRecommendation(result.recommendation);

    drawPieChart(result.finance);

    drawBarChart(result.finance);

    updateProgress(

        result.finance,

        result.planning

    );

    updateFinancialStatus(result.finance);

    updatePlanning(result.planning);

}

function renderRules(rules){

    const list = document.getElementById("ruleList");

    list.innerHTML="";

    if(rules.length===0){

        list.innerHTML="<li>Tidak ada peringatan.</li>";

        return;

    }

    rules.forEach(rule=>{

        list.innerHTML +=

        `<li>${rule.message}</li>`;

    });

}

function renderRecommendation(data){

    const list = document.getElementById("recommendationList");

    list.innerHTML="";

    data.forEach(item=>{

        list.innerHTML +=

        `<li>${item}</li>`;

    });

}

function updateFinancialStatus(finance){

    const ratio =

        finance.total_pengeluaran /

        finance.pemasukan;

    const status =

        document.getElementById("financialStatus");

    const message =

        document.getElementById("financialMessage");

    if(ratio<=0.7){

        status.innerHTML="🟢 Baik";

        status.className="text-success";

        message.innerHTML=

        "Keuangan Anda sehat.";

    }

    else if(ratio<=0.9){

        status.innerHTML="🟡 Waspada";

        status.className="text-warning";

        message.innerHTML=

        "Pengeluaran mulai tinggi.";

    }

    else{

        status.innerHTML="🔴 Defisit";

        status.className="text-danger";

        message.innerHTML=

        "Segera kurangi pengeluaran.";

    }

}

function updatePlanning(plan){

    document
    .getElementById("monthlyTarget")
    .innerHTML=

    rupiah(plan.target_per_bulan);

    document
    .getElementById("planningGap")
    .innerHTML=

    rupiah(plan.kekurangan);

    document
    .getElementById("planningStatus")
    .innerHTML=

    plan.cukup

    ?

    "✅ Tercapai"

    :

    "⚠ Belum";
}