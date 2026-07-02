const API = {
    async analyze(data){
        const response = await fetch("/api/analyze",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(data)
        });
        if(!response.ok){
            throw new Error("Gagal melakukan analisis.");
        }
        return await response.json();
    },
    async history(){
        const response = await fetch("/api/history");
        return await response.json();
    },
    async deleteHistory(id){
        const response = await fetch(`/api/history/${id}`,{
            method:"DELETE"
        });
        return await response.json();
    }
};