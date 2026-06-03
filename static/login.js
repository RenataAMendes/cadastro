document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");

    form.addEventListener("submit", (event) => {
        const emailInput = document.getElementById("email");
        const senhaInput = document.getElementById("senha");

        const email = emailInput.value.trim();
        const senha = senhaInput.value.trim();

        if (email === "" || senha === "") {
            event.preventDefault();
            alert("Por favor, preencha todos os campos.");
            return;
        }

        if (senha.length < 6) {
            event.preventDefault();
            alert("A senha deve ter no mínimo 6 caracteres.");
            return;
        }

    });
});