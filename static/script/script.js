var indexImage = 0

let img = document.querySelector(".imgage__bio");
let countElem = document.querySelector(".count");

let uploadFile = null;
let colors = null;

function upload(){
    let file = document.querySelector("#file").files[0];

    let reader = new FileReader();
    reader.onload = function(){
        let resBase64 = reader.result;
        console.log(resBase64);
        img.src = resBase64;

        let xhr = new XMLHttpRequest();
        xhr.open('POST', "/getcolors");
        xhr.onload = function(){
            let response = JSON.parse(xhr.response);
            indexImage = 0;
            
            uploadFile = resBase64;
            colors = response;

            getMask();

            console.log(response);
            
            
        }
        xhr.send(JSON.stringify({"file": resBase64}));

    }
    reader.readAsDataURL(file);
}

function getMask(){
    let xhr = new XMLHttpRequest();
    xhr.open('POST', "/upload");
    xhr.onload = function(){
        let response = JSON.parse(xhr.response);
        response["file"] = "data:image/jpeg;base64," + response["file"];
        img.src = response["file"];
        console.log(response);
        countElem.textContent = response["count"];


    }
    xhr.send(JSON.stringify({"file": uploadFile, "color": colors[indexImage]}));
}

function next(){
    if(indexImage + 1 < colors.length){
        indexImage++;
    }else{
        indexImage = 0;
    }
    
    getMask();
}

function back(){

    if(indexImage - 1 >= 0){
        indexImage--;
    }else{
        indexImage = colors.length - 1;
    }
    
    getMask();

}