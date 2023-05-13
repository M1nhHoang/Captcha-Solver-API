const upLoad_image = document.getElementById('upload_Image');
const predict      = document.getElementById('predict');
const result       = document.getElementById('result');

upLoad_image.addEventListener('change', (event) => {
    // last img class
    try {
        var has_image = document.getElementsByClassName('img_display')[0];
        has_image.parentNode.removeChild(has_image); 
    }
    catch{
        // pass
    }
    // upload image
    if (upLoad_image.files.length > 0) {
        var fileToLoad = upLoad_image.files[0]
        // check size image
        if (fileToLoad.size/1024 > 50) {
            alert('Hình ảnh phải nhỏ hơn 50 KB');
        }
        else {
            var fileReader = new FileReader();
            fileReader.readAsDataURL(fileToLoad)
            fileReader.onload = function(fileLoaderEvent){
                var srcData = fileLoaderEvent.target.result;
                var htmlString = `<img src="${srcData}" alt="${fileToLoad.name}" class="img_display""/>`
                var resultElement = document.getElementsByClassName('imageDemo_display')[0]
                resultElement.insertAdjacentHTML('afterbegin', htmlString)  
            }
        }
    }
});

predict.addEventListener('click', (event) => {
    var title = document.title.split(" ");
    try {
        var img = document.getElementsByClassName('img_display')[0].src;
    }
    catch {
        result.innerHTML = "<p style='color: red'>Xin hãy chọn hình ảnh!</p>";;
    }
    
    var url = "/getText?captcha="+title[1]+"&type="+title[3]+"&image="+img;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) {
            showResult(xhttp.responseText);
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
    predict.disabled = true;

    function showResult(pred) {
        result.innerHTML = pred;
        predict.disabled = false;
    }
    
});








// const boxes = document.querySelectorAll('.commonitem_thumb_textcaptcha');
// const bts = document.getElementsByClassName('BtItem_thumb');

// boxes.forEach(box => {
//   box.addEventListener('mouseover', function handleClick(event) {

//     setTimeout(box.style.opacity = 0.5);
//     // console.log(bts);
//     box.querySelector('.BtItem_thumb').style.opacity = 1;


//     // box.setAttribute('style', 'background-color: yellow;');
//   });
//   box.addEventListener('mouseout', function handleClick(event) {

//     setTimeout(box.style.opacity = 1);
//     box.querySelector('.BtItem_thumb').style.opacity = 0;


//     // box.setAttribute('style', 'background-color: yellow;');
//   });
// });
