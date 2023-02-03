const client_list = {
        "Papa Pita Bakery": "Papa Pita Bakery",
        "PBM": "PBM",
        "Novatime": "Novatime",
        "Nutraceutical": "Nutraceutical",
        "Maximus": "Maximus"
}

const phrases = ["Crack the Sky", "Let Your Hammer Fly", "Call Down the Lightning",
"To Valhalla and Back", "Release Asgaard's Fury"]

let phraseIndex = Math.floor(Math.random() * phrases.length)

$(() => {
    // Initial load function.
    // Checks if the backend is up and running.
    // Displays an error if it is not.
    $.ajax({
        url: 'http://127.0.0.1:5000/',
        type: 'GET',
        cache: false,
        contentType: false,
        processData: false,
        tryCount : 0,
        retryLimit : 3,
        success : () => {
            $('#submit-button').text(phrases[phraseIndex]) 
            $('#overlay').fadeOut()
        },
        error: (xhr, textStatus, errorThrown) => {
            if(textStatus == 'timeout') {
                this.tryCount++;
                if(this.tryCount <= this.retryLimit) {
                    $.ajax(this);
                    return;
                }
                $('#overlay').fadeOut()
                $('#submit-button').prop("disabled", true)
                $('#submit-button').text("Error: Disabled") 
                let errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">Error: Please reload the page and try again.</p>`
                $('#errors').append(errorHTML)
                return;
            }
            if(xhr.status == 500) {
                $('#overlay').fadeOut()
                $('#submit-button').prop("disabled", true)
                $('#submit-button').text("Error: Disabled") 
                let errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">Error: Please reload the page and try again.</p>`
                $('#errors').append(errorHTML)
            }else{
                $('#overlay').fadeOut()
                $('#submit-button').prop("disabled", true)
                $('#submit-button').text("Error: Disabled") 
                let errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">Error: Please reload the page and try again.</p>`
                $('#errors').append(errorHTML)
            }
        }
    })

    // Sets the select to have the current supported clients/vms'
    $.each(client_list, function(key, value) {   
        $('#client_select')
            .append($("<option></option>")
                       .attr("value", key)
                       .text(value)); 
   });

    //Form submission handler
    $('form').on('submit', (e) => {
        e.preventDefault();

        let formData = new FormData();
        let client = (document.getElementById('client_select'));
        let upload = document.querySelector('#convert_files');
        let url = 'http://127.0.0.1:5000/'
        for (let f of upload.files) {
            formData.append("file", f)
        }
        formData.append("client", client.options[client.selectedIndex].text)

        let req = new XMLHttpRequest();
        req.open('POST', url);
        req.responseType = 'arraybuffer';
        req.onload = (e) => {
            let contentDispo = e.currentTarget.getResponseHeader('Content-Disposition');
            let blob = new Blob([this.response], {type: 'application/octet-stream'})
            let fileName = contentDispo.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)[1];
            let file = new File([blob], fileName, {type: contentDispo})
            let a = document.createElement('a')
            let url = window.URL.createObjectURL(file)
            a.setAttribute('download', 'file')
            console.log(e)
            a.href = url;
            a.download = fileName
            document.body.append(a)
            a.click()
            a.remove()
            window.URL.revokeObjectURL(url)
        }
        req.send(formData)

        // console.log(req)

        // $.ajax({
        //     url: 'http://127.0.0.1:5000/',
        //     type: 'POST',
        //     data: formData,
        //     cache: false,
        //     contentType: false,
        //     processData: false,
        //     xhrFields: {
        //         responseTyep: 'blob'
        //     },
            // success: (res) => {
            //     window.open(res.url, '_blank')
            // }
        //     success: (data) => {
        //         let a = document.createElement('a')
        //         let url = window.URL.createObjectURL(new Blob([data], {type: 'application/zip'}))
        //         a.href = url;
        //         a.download = data.filename
        //         document.body.append(a)
        //         a.click()
        //         a.remove()
        //         window.URL.revokeObjectURL(url)
        //     }
        // })
        // .done((res) => {
        //     let URL = window.URL || window.webkitURL;
        //     let downloadURL = URL.createObjectURL(res)
            // console.log(res)
            // let a = document.createElement('a');
            // let binaryData = []
            // binaryData.push(res)
            // a.href = window.URL.createObjectURL(new Blob(binaryData, {type: "application/zip"}))
            // a.download = "imports.zip"
            // a.style.display = 'none';
            // document.body.appendChild(a)
            // a.click();

        // })
    });
});