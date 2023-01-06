document.getElementById("encryptCheck").addEventListener("click", showEncryptForm);

function showEncryptForm() {
    var checkBox = document.getElementById("encryptCheck");
    var encryptForm = document.getElementById("encryptForm");

    if (checkBox.checked == true){
      encryptForm.className = "showform";
    } else {
      encryptForm.className = "hiddenform";
    }
}

