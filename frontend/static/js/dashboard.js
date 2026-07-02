function updateClock() {

    const greetingEl = document.getElementById("greeting");
    const dateEl = document.getElementById("currentDate");
    const timeEl = document.getElementById("currentTime");

    // These elements only exist on the dashboard page.
    if (!greetingEl || !dateEl || !timeEl) {
        return;
    }

    const now = new Date();
    const jam = now.getHours();
    let greeting = "";

    if (jam < 11) {
        greeting = "Selamat Pagi ☀️";
    } else if (jam < 15) {
        greeting = "Selamat Siang 🌤";
    } else if (jam < 18) {
        greeting = "Selamat Sore 🌥";
    } else {
        greeting = "Selamat Malam 🌙";
    }

    greetingEl.innerHTML = greeting;

    dateEl.innerHTML = now.toLocaleDateString("id-ID", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
    });

    timeEl.innerHTML = now.toLocaleTimeString("id-ID");
}

updateClock();

setInterval(updateClock, 1000);
