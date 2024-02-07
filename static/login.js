
//function used to switch between login and signup form
function donthaveaccount(value){
    frmClass = "loginform";
    var forms = [document.getElementById("loginForm"), document.getElementById("signupForm")];
    //checking if value is saying login or signup to switch to
    if(value=="login"){
        forms[0].setAttribute("class",frmClass);
        forms[1].setAttribute("class","disable");
    }
    else if(value=="signup"){
        forms[1].setAttribute("class",frmClass);
        forms[0].setAttribute("class","disable");
    }
}