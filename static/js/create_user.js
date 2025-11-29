document.addEventListener("DOMContentLoaded", function () {
    const groupSelect = document.getElementById("id_user_group");
    const licenseField = document.getElementById("license-count-field");

    function updateVisibility() {
        const value = groupSelect.value;

        if (value === "ClientAdmin" || value === "ResellerAdmin") {
            licenseField.classList.remove("d-none");
        } else {
            licenseField.classList.add("d-none");
            const input = licenseField.querySelector("input");
            if (input) input.value = "";
        }
    }

    groupSelect.addEventListener("change", updateVisibility);
    updateVisibility();
});