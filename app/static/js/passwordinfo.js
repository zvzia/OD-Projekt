const password = document.getElementById('password');
    const passwordRetyped = document.getElementById('password_retyped');
    const info = document.getElementById('info');

    const username = document.getElementById('username');
    const email = document.getElementById('email');
    info.innerHTML = "You have to insert all information";
    document.getElementById("submitBtn").disabled = true;

    var special = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;

    const inputHandler = function(e) {
        const passwordVal = document.getElementById('password').value
        if(document.getElementById('username').value == "" || document.getElementById('email').value == "" || document.getElementById('password').value == ""){
            info.innerHTML = "You have to insert all information";
            document.getElementById("submitBtn").disabled = true;
        }else if(passwordVal.length < 10){ //dlugosc
            info.innerHTML = "Your password should contain at least 10 characters";
                document.getElementById("submitBtn").disabled = true;
        }else if(!/[A-Z]/.test(passwordVal)){ //duze litery
            info.innerHTML = "Your password should contain at least one uppercase letter";
            document.getElementById("submitBtn").disabled = true;
        }else if(!/[a-z]/.test(passwordVal)){ // male litery
            info.innerHTML = "Your password should contain at least one lowercase letter";
            document.getElementById("submitBtn").disabled = true;
        }else if(!/\d/.test(passwordVal)){ //cyfry
            info.innerHTML = "Your password should contain at least one number";
            document.getElementById("submitBtn").disabled = true;
        }else if(!special.test(passwordVal)){ //znaki spcjalne
            info.innerHTML = "Your password should contain at least one special character";
            document.getElementById("submitBtn").disabled = true;
        }else if(document.getElementById('password').value != document.getElementById('password_retyped').value){
            info.innerHTML = "Password doesnt match";
            document.getElementById("submitBtn").disabled = true;
        }else{
            info.innerHTML = "";
            document.getElementById("submitBtn").disabled = false;
        }
    }

    const inputHandlerUserInfo = function(e) {
        if(document.getElementById('username').value == "" || document.getElementById('email').value == ""){
            info.innerHTML = "You have to insert all information";
            document.getElementById("submitBtn").disabled = true;
        }else{
            info.innerHTML = "";
            document.getElementById("submitBtn").disabled = false;
        }
    }

    username.addEventListener('input', inputHandler);
    email.addEventListener('input', inputHandler);


    password.addEventListener('input', inputHandler);
    password.addEventListener('propertychange', inputHandler);

    passwordRetyped.addEventListener('input', inputHandler);
    passwordRetyped.addEventListener('propertychange', inputHandler);