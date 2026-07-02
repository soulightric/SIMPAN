document.addEventListener("DOMContentLoaded",loadHistory);

let historyData=[];

async function loadHistory(){

    historyData=await API.history();

    renderHistory(historyData);

}

function renderHistory(data){

    const table=document.getElementById("historyTable");

    table.innerHTML="";

    data.forEach(item=>{

        table.innerHTML+=`

<tr>

<td>${item.id}</td>

<td>${item.created_at}</td>

<td>${rupiah(item.pemasukan)}</td>

<td>${rupiah(item.total_pengeluaran)}</td>

<td>${rupiah(item.saldo)}</td>

<td>${rupiah(item.target)}</td>

<td>

<button

class="btn btn-danger btn-sm"

onclick="hapus(${item.id})">

Hapus

</button>

</td>

</tr>

`;

    });

}

async function hapus(id){

    if(!confirm("Yakin ingin menghapus?"))

    return;

    await API.deleteHistory(id);

    loadHistory();

}

document

.getElementById("searchHistory")

.addEventListener("keyup",function(){

const keyword=this.value.toLowerCase();

const hasil=

historyData.filter(item=>

item.created_at.toLowerCase().includes(keyword)

||

item.id.toString().includes(keyword)

);

renderHistory(hasil);

});

function downloadCSV(){

let csv=

"ID,Tanggal,Pemasukan,Pengeluaran,Saldo,Target\n";

historyData.forEach(item=>{

csv+=

`${item.id},${item.created_at},${item.pemasukan},${item.total_pengeluaran},${item.saldo},${item.target}\n`;

});

const blob=new Blob([csv],{

type:"text/csv"

});

const link=document.createElement("a");

link.href=

URL.createObjectURL(blob);

link.download="history.csv";

link.click();

}