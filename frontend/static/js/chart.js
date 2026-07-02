let pieChart = null;
let barChart = null;

function drawPieChart(finance){

    const ctx = document
        .getElementById("pieChart")
        .getContext("2d");

    if(pieChart){

        pieChart.destroy();

    }

    pieChart = new Chart(ctx,{

        type:"pie",

        data:{

            labels:[

                "Makanan",
                "Transportasi",
                "Pendidikan",
                "Hiburan",
                "Lainnya"

            ],

            datasets:[{

                data:[

                    finance.makanan,
                    finance.transportasi,
                    finance.pendidikan,
                    finance.hiburan,
                    finance.lainnya

                ]

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                legend:{

                    position:"bottom"

                }

            }

        }

    });

}

function drawBarChart(finance){

    const ctx = document
        .getElementById("barChart")
        .getContext("2d");

    if(barChart){

        barChart.destroy();

    }

    barChart = new Chart(ctx,{

        type:"bar",

        data:{

            labels:[

                "Pemasukan",
                "Pengeluaran"

            ],

            datasets:[{

                label:"Nominal",

                data:[

                    finance.pemasukan,

                    finance.total_pengeluaran

                ]

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            scales:{

                y:{

                    beginAtZero:true

                }

            }

        }

    });

}

function updateProgress(finance,plan){

    let persen =

        (finance.saldo/plan.target_tabungan)*100;

    if(persen>100){

        persen=100;

    }

    if(persen<0){

        persen=0;

    }

    const bar=

        document.getElementById("targetProgress");

    bar.style.width=

        persen+"%";

    bar.innerHTML=

        persen.toFixed(1)+"%";

}