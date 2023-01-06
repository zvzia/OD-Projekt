function showEncryptForm() {
    var checkBox = document.getElementById("encryptCheck");
    var encryptForm = document.getElementById("encryptForm");

    if (checkBox.checked == true){
      encryptForm.style.display = "block";
    } else {
      encryptForm.style.display = "none";
    }
}