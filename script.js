var dvd_list = document.querySelector("#DVD-list");

var editHeader = document.querySelector("#addheader");

var addButton = document.querySelector("#addButton");
var invisEditButton = document.querySelector("#editButton");

var titleInputForm = document.querySelector("#titleform");
var ratingInputForm = document.querySelector("#ratingform");
var priceInputForm = document.querySelector("#priceform");
var dateInputForm = document.querySelector("#dateform");
var genreInputForm = document.querySelector("#genreform");

var signInButton = document.querySelector("#signinbutton");
var registerButton = document.querySelector("#registerbutton");
var emailSignInForm = document.querySelector("#emailsigninform");
var passwordSignInForm = document.querySelector("#passwordsigninform");

var fnameForm = document.querySelector("#fnameform");
var lnameForm = document.querySelector("#lnameform");
var emailRegisterForm = document.querySelector("#emailregisterform");
var passwordRegisterForm = document.querySelector("#passwordregisterform");
var passwordConfirmForm = document.querySelector("#passwordconfirmform");

var errorIncompleteSignIn = document.querySelector("#incompleteinfoerrorsignin");
var errorIncompleteRegister = document.querySelector("#incompleteinfoerrorregister");
var errorMismatchedPasswords = document.querySelector("#passwordmatcherror");
var errorUserExistsAlready = document.querySelector("#useralreadyexistserror");
var errorIncorrectPassword = document.querySelector("#incorrecterror");

var notLoggedInDiv = document.querySelector("#nosession");
var loggedInDiv = document.querySelector("#hidewrapper");

var BASEURL = "https://dvd-inventory.herokuapp.com"


var getDVDs = function(){
    fetch(BASEURL + "/dvds", {
        credentials: "include"
    }).then(function(response){
        if(response.status == 200){
            notLoggedInDiv.style.display = "none";
            loggedInDiv.style.display = "block";
            
            response.json().then(function(data){
                data.forEach(function(dvd){
                    var newListItem = document.createElement("li");
                    
                    var dvdTitle = document.createElement("h3");
                    var dvdRating = document.createElement("div");
                    var dvdPrice = document.createElement("div")
                    var dvdDate = document.createElement("div")
                    var dvdGenre = document.createElement("div")

                    dvdTitle.innerHTML = dvd.title;
                    dvdRating.innerHTML = "Rated " + dvd.rating;
                    dvdPrice.innerHTML = "$" + dvd.price;
                    dvdDate.innerHTML = "Acquired on " + dvd.date;
                    dvdGenre.innerHTML = "Genre: " + dvd.genre;

                    newListItem.appendChild(dvdTitle);
                    newListItem.appendChild(dvdRating);
                    newListItem.appendChild(dvdPrice);
                    newListItem.appendChild(dvdDate);
                    newListItem.appendChild(dvdGenre);

                    var deleteButton = document.createElement("button");
                    deleteButton.innerHTML = "Delete";
                    deleteButton.onclick = function(){
                        console.log("I got clicked.")
                        if(confirm("Are you sure you want to delete " + dvd.title + "?")){
                            deleteDVD(dvd.inv);
                        }
                    };

                    var editButton = document.createElement("button");
                    editButton.innerHTML = "Edit";
                    editButton.onclick = function(){
                        console.log("I got clicked.")
                        invisEditButton.style.visibility = 'visible';
                        addButton.style.visibility = "hidden";

                        editHeader.innerHTML = "EDITING...";
                    
                        titleInputForm.value = dvd.title;
                        ratingInputForm.value = dvd.rating;
                        priceInputForm.value = dvd.price;
                        dateInputForm.value = dvd.date;
                        genreInputForm.value = dvd.genre;

                        invisEditButton.onclick = function (){
                            editDVD(dvd.inv);
                        }
                    }
                    newListItem.appendChild(deleteButton);
                    newListItem.appendChild(editButton);
                    dvd_list.appendChild(newListItem);
                });
            });
        } else {
            notLoggedInDiv.style.display = "inline";
            loggedInDiv.style.display = "none";
        }
    });
};

signInButton.onclick = function(){
    if((emailSignInForm.value.trim() == '') || (passwordSignInForm.value.trim() == '')){
        resetErrors();
        errorIncompleteSignIn.style.display = "inline";
    } else {
        var enteredEmail = emailSignInForm.value.trim();
        var enteredPassword = passwordSignInForm.value.trim();

        var rawBody = "email=" + encodeURIComponent(enteredEmail);
        rawBody += "&" + "password=" + encodeURIComponent(enteredPassword);

        fetch(BASEURL + "/sessions",{
            method: "POST",
            credentials: "include",
            body: rawBody,
            headers:{
                "Content-Type": "application/x-www-form-urlencoded",
            }
        }).then(function(response){
            if(response.status == 401){
                resetErrors();
                errorIncorrectPassword.style.display = "inline";
            } else if(response.status == 201) {
                resetErrors();
                emailSignInForm.value = '';
                //test purposes!
                passwordSignInForm.value = 'authentication successful.';
                getDVDs();
            } else {
                resetErrors();
                emailSignInForm.value = '';
                //test purposes!
                passwordSignInForm.value = 'this shouldnt ever be seen.';
            }
        })
    }
    resetPasswordForms();
};

registerButton.onclick = function(){
    resetErrors();
    if((fnameForm.value.trim() == '') || (lnameForm.value.trim() == '') || (emailRegisterForm.value.trim() == '') || (passwordRegisterForm.value.trim() == '') || (passwordConfirmForm.value.trim() == '')){
        errorIncompleteRegister.style.display = "inline";
    } else if(passwordRegisterForm.value.trim() != passwordConfirmForm.value.trim()){
        errorMismatchedPasswords.style.display = "inline";
    } else {
        var newFname = fnameForm.value.trim();
        var newLname = lnameForm.value.trim();
        var newEmail = emailRegisterForm.value.trim();
        var newPassword = passwordRegisterForm.value.trim();

        var rawBody = "fname=" + encodeURIComponent(newFname);
        rawBody += "&" + "lname=" + encodeURIComponent(newLname);
        rawBody += "&" + "email=" + encodeURIComponent(newEmail);
        rawBody += "&" + "password=" + encodeURIComponent(newPassword);

        fetch(BASEURL + "/users",{
            method: "POST",
            credentials: "include",
            body: rawBody,
            headers:{
                "Content-Type": "application/x-www-form-urlencoded",
            }
        }).then(function(response){
            if(response.status == 422){
                resetErrors();
                errorUserExistsAlready.style.display = "inline";
            } else{
                fnameForm.value = '';
                lnameForm.value = '';
                emailRegisterForm.value = '';
                passwordRegisterForm.value = '';
                passwordConfirmForm.value = '';
                resetErrors();
                fetch(BASEURL + "/sessions",{
                    method: "POST",
                    credentials: "include",
                    body: rawBody,
                    headers:{
                        "Content-Type": "application/x-www-form-urlencoded",
                    }
                }).then(function(response){
                    getDVDs();
                })
            }
        });
    }
    resetPasswordForms();
};

addButton.onclick = function(){
    if((titleInputForm.value.trim() == '') || (ratingInputForm.value.trim() == '') || (priceInputForm.value.trim() == '') || (dateInputForm.value.trim() == '') || (genreInputForm.value.trim() == '')){
        alert("Please fill out all fields.")
    } else {
        var newTitle = titleInputForm.value;
        var newRating = ratingInputForm.value;
        var newPrice = priceInputForm.value;
        var newDate = dateInputForm.value;
        var newGenre = genreInputForm.value;

        var rawBody = "title=" + encodeURIComponent(newTitle);
        rawBody += "&" + "rating=" + encodeURIComponent(newRating);
        rawBody += "&" + "price=" + encodeURIComponent(newPrice);
        rawBody += "&" + "date=" + encodeURIComponent(newDate);
        rawBody += "&" + "genre=" + encodeURIComponent(newGenre);

        fetch(BASEURL + "/dvds", {
            method: "POST",
            credentials: "include",
            body: rawBody,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            }
        }).then(function(response){
            dvd_list.innerHTML = "";

            titleInputForm.value = '';
            ratingInputForm.value = '';
            priceInputForm.value = '';
            dateInputForm.value = '';
            genreInputForm.value = '';

            getDVDs();
        });
    }
};


var deleteDVD = function(inv){
    fetch(BASEURL + "/dvds/" + inv, {
        method: "DELETE",
        credentials: "include"
    }).then(function(response){
        dvd_list.innerHTML = "";
        getDVDs();
    })
};

var resetErrors = function(){
    errorIncompleteRegister.style.display = "none";
    errorIncompleteSignIn.style.display = "none";
    errorMismatchedPasswords.style.display = "none";
    errorUserExistsAlready.style.display = "none";
    errorIncorrectPassword.style.display = "none";
};

var resetPasswordForms = function(){
    passwordConfirmForm.value = '';
    passwordRegisterForm.value = '';
    passwordSignInForm.value = '';
}

var editDVD = function(inv){
    var newTitle = titleInputForm.value;
    var newRating = ratingInputForm.value;
    var newPrice = priceInputForm.value;
    var newDate = dateInputForm.value;
    var newGenre = genreInputForm.value;

    var rawBody = "title=" + encodeURIComponent(newTitle);
    rawBody += "&" + "rating=" + encodeURIComponent(newRating);
    rawBody += "&" + "price=" + encodeURIComponent(newPrice);
    rawBody += "&" + "date=" + encodeURIComponent(newDate);
    rawBody += "&" + "genre=" + encodeURIComponent(newGenre);

    fetch(BASEURL + "/dvds/" + inv, {
        method: "PUT",
        credentials: "include",
        body: rawBody,
        headers:{
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }).then(function(response){
        dvd_list.innerHTML = "";

        titleInputForm.value = "";
        ratingInputForm.value = "";
        priceInputForm.value = "";
        dateInputForm.value = "";
        genreInputForm.value = "";

        invisEditButton.style.visibility = "hidden";
        addButton.style.visibility = "visible";

        editHeader.innerHTML = "Add new DVD to inventory:"

        getDVDs();
    })
}

getDVDs();