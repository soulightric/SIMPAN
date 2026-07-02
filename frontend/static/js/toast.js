function showToast(message){
    document.getElementById("toastBody").innerHTML=message;
    const toast = new bootstrap.Toast(document.getElementById("mainToast"));
    toast.show();
}