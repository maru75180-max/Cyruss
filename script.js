document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const businessCards = document.querySelectorAll(".business-card");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const value = this.value.toLowerCase().trim();
            businessCards.forEach(function (card) {
                card.style.display = card.innerText.toLowerCase().includes(value) ? "" : "none";
            });
        });
    }

    const addButton = document.getElementById("addBusinessBtn");
    const addModal = document.getElementById("addModal");
    const closeAddModal = document.getElementById("closeAddModal");

    if (addButton && addModal) addButton.addEventListener("click", () => addModal.classList.add("show"));
    if (closeAddModal && addModal) closeAddModal.addEventListener("click", () => addModal.classList.remove("show"));

    const editModal = document.getElementById("editModal");
    const closeEditModal = document.getElementById("closeEditModal");

    document.querySelectorAll(".edit-btn").forEach(function (button) {
        button.addEventListener("click", function () {
            if (!editModal) return;
            const form = document.getElementById("editForm");
            form.action = "/edit/" + this.dataset.id;

            document.getElementById("edit_business_name").value = this.dataset.name || "";
            document.getElementById("edit_owner_name").value = this.dataset.owner || "";
            document.getElementById("edit_phone").value = this.dataset.phone || "";
            document.getElementById("edit_email").value = this.dataset.email || "";
            document.getElementById("edit_address").value = this.dataset.address || "";
            document.getElementById("edit_category").value = this.dataset.category || "";
            document.getElementById("edit_details").value = this.dataset.details || "";
            document.getElementById("edit_facebook").value = this.dataset.facebook || "";
            document.getElementById("edit_instagram").value = this.dataset.instagram || "";
            document.getElementById("edit_website").value = this.dataset.website || "";
            document.getElementById("edit_logo_url").value = this.dataset.logo || "";

            editModal.classList.add("show");
        });
    });

    if (closeEditModal && editModal) closeEditModal.addEventListener("click", () => editModal.classList.remove("show"));

    [addModal, editModal].forEach(function (modal) {
        if (modal) modal.addEventListener("click", function (event) {
            if (event.target === modal) modal.classList.remove("show");
        });
    });

    document.querySelectorAll(".delete-form").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (!confirm("Are you sure you want to delete this business?")) event.preventDefault();
        });
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            if (addModal) addModal.classList.remove("show");
            if (editModal) editModal.classList.remove("show");
        }
    });
});
