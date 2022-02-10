let passwordField = document.getElementById('Rpassword');
passwordField.addEventListener('input', () => {
    if (passwordField.value.length == 0) {
        passwordField.style.backgroundColor = '';
    }
    else if (passwordField.value.length <= 3) {
        passwordField.style.backgroundColor = '#ff4d4d';
    }
    else if (passwordField.value.length > 3 & passwordField.value.length < 6) {
        passwordField.style.backgroundColor = 'yellow';
    }
    else {
        passwordField.style.backgroundColor = '#66ff66';
    }
})