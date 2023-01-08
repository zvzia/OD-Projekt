const password = document.getElementById('password');
const passwordRetyped = document.getElementById('password_retyped');
const info = document.getElementById('info');

info.innerHTML = "You have to insert all information";
document.getElementById("submitBtn").disabled = true;

var special = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;


const inputHandler = function(e) {
    const passwordVal = document.getElementById('password').value
    if(document.getElementById('password').value == ""){
        info.innerHTML = "You have to insert all information";
        document.getElementById("submitBtn").disabled = true;
    }else if(document.getElementById('password').value != document.getElementById('password_retyped').value){
        info.innerHTML = "Password doesnt match";
        document.getElementById("submitBtn").disabled = true;
    }else if(passwordVal.length < 10 || !/[A-Z]/.test(passwordVal) || !/[a-z]/.test(passwordVal) || !/\d/.test(passwordVal) || !special.test(passwordVal)){
        document.getElementById("submitBtn").disabled = true;
    }else{
        info.innerHTML = "";
        document.getElementById("submitBtn").disabled = false;
    }

    if(passwordVal.length < 10){ //dlugosc
        document.getElementById("length").className = "infoRed";
    }else {
        document.getElementById("length").className = "infoGreen";
    }

    if(!/[A-Z]/.test(passwordVal)){ //duze litery
        document.getElementById("upperCase").className = "infoRed";
    }else {
        document.getElementById("upperCase").className = "infoGreen";
    }

    if(!/[a-z]/.test(passwordVal)){ // male litery
        document.getElementById("lowerCase").className = "infoRed";
    }else {
        document.getElementById("lowerCase").className = "infoGreen";
    }

    if(!/\d/.test(passwordVal)){ //cyfry
        document.getElementById("numbers").className = "infoRed";
    }else {
        document.getElementById("numbers").className = "infoGreen";
    }

    if(!special.test(passwordVal)){ //znaki spcjalne
        document.getElementById("specialChar").className = "infoRed";
    }else {
        document.getElementById("specialChar").className = "infoGreen";
    }
    
}


password.addEventListener('input', inputHandler);
password.addEventListener('propertychange', inputHandler);

passwordRetyped.addEventListener('input', inputHandler);
passwordRetyped.addEventListener('propertychange', inputHandler);