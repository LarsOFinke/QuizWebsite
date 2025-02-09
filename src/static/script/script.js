function togglePassword() {
    const passwordInput = document.getElementById('password');
    const showPasswordCheckbox = document.getElementById('showPassword');

    // Toggle the type attribute based on the checkbox state
    if (showPasswordCheckbox.checked) {
        passwordInput.type = 'text'; // Show password
    } else {
        passwordInput.type = 'password'; // Hide password
    }
}

function togglePasswords() {
    const passwordInput = document.getElementById('password');
    const passwordConfirm = document.getElementById('password2')
    const showPasswordCheckbox = document.getElementById('showPassword');

    // Toggle the type attribute based on the checkbox state
    if (showPasswordCheckbox.checked) {
        passwordInput.type = 'text'; // Show password
        passwordConfirm.type = 'text';
    } else {
        passwordInput.type = 'password'; // Hide password
        passwordConfirm.type = 'password';
    }
}

