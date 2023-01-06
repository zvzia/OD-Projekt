function showEncryptForm() {
    var checkBox = document.getElementById("encryptCheck");
    var encryptForm = document.getElementById("encryptForm");

    if (checkBox.checked == true){
      encryptForm.classList.add = "showform"
      encryptForm.classList.remove = "hiddenform"
    } else {
      encryptForm.classList.add = "hiddenform"
      encryptForm.classList.remove = "showform"
    }
}