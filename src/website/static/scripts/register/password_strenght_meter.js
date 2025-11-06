//password strenght logic
document.addEventListener("DOMContentLoaded", function() {
    const passwordTextBox = document.getElementById("password_register");
    if (!passwordTextBox) return;

    passwordTextBox.addEventListener("input", function() {
        const password = passwordTextBox.value;
        let strength = 0;

        if (password.length >= 8) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/\d/.test(password)) strength++;
        if (/[@$!%*?&]/.test(password)) strength++;

        let color = "";
        if (strength <= 2) {
            color = "red";
        } else if (strength <= 4) {
            color = "orange";
        } else {
            color = "green";
        }

        // passwordTextBox.style.borderColor = color;
        passwordTextBox.style.boxShadow = `0 0 5px ${color}`;
    });

    passwordTextBox.addEventListener("blur",function(){
        
        passwordTextBox.style.boxShadow=`inset 0 0 5px rgba(255, 255, 255, 0.1)`
        
    });
});
