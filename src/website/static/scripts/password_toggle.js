// checkbox logic 
document.addEventListener("DOMContentLoaded", function () {

    const checkboxes = document.getElementsByName("show_pass");
   
    Array.from(checkboxes).forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const form = checkbox.closest("form");
            if (!form) return;

            const passwordInput = form.querySelector('input[name="password"]');
            if (!passwordInput) return;

            if (checkbox.checked) {
                passwordInput.type = "text";
            } else {
                passwordInput.type = "password";
            }
        });
    });

});
