(function () {
    const toggle = document.getElementById("toggleSidebar");
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");
    const backdrop = document.getElementById("sidebarBackdrop");

    if (!sidebar) return;

    const MOBILE_BREAKPOINT = 992;
    const isMobile = () => window.innerWidth < MOBILE_BREAKPOINT;

    // --- Restore collapsed state (desktop only) ---
    if (localStorage.getItem("sidebarCollapsed") === "1" && !isMobile()) {
        sidebar.classList.add("collapsed");
        if (content) content.classList.add("expanded");
    }

    function openMobile() {
        sidebar.classList.add("show");
        if (backdrop) backdrop.classList.add("show");
    }

    function closeMobile() {
        sidebar.classList.remove("show");
        if (backdrop) backdrop.classList.remove("show");
    }

    function toggleSidebar() {
        if (isMobile()) {
            sidebar.classList.contains("show") ? closeMobile() : openMobile();
        } else {
            sidebar.classList.toggle("collapsed");
            if (content) content.classList.toggle("expanded");
            localStorage.setItem(
                "sidebarCollapsed",
                sidebar.classList.contains("collapsed") ? "1" : "0"
            );
        }
    }

    if (toggle) toggle.addEventListener("click", toggleSidebar);

    // Close when tapping the backdrop (mobile)
    if (backdrop) backdrop.addEventListener("click", closeMobile);

    // Close after choosing a menu item on mobile
    sidebar.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
            if (isMobile()) closeMobile();
        });
    });

    // Close on Escape
    document.addEventListener("keydown", e => {
        if (e.key === "Escape" && isMobile()) closeMobile();
    });

    // Reset mobile state when resizing up to desktop
    window.addEventListener("resize", () => {
        if (!isMobile()) closeMobile();
    });

    // --- Highlight the active menu item based on the current URL ---
    const path = window.location.pathname;
    sidebar.querySelectorAll("a").forEach(link => {
        link.classList.remove("active");
        const href = link.getAttribute("href");
        if (href && href !== "#" &&
            (href === path || (href !== "/" && path.startsWith(href)))) {
            link.classList.add("active");
        }
    });
    if (path === "/") {
        const home = sidebar.querySelector('a[href="/"]');
        if (home) home.classList.add("active");
    }
})();
