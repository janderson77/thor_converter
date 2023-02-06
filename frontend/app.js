const client_list = {
    "Papa Pita Bakery": "Papa Pita Bakery",
    "PBM": "PBM",
    "Novatime": "Novatime",
    "Nutraceutical": "Nutraceutical",
    "Maximus": "Maximus"
};

const phrases = ["Crack the Sky", "Let Your Hammer Fly", "Call Down the Lightning",
    "To Valhalla and Back", "Release Asgaard's Fury"];

let phraseIndex = Math.floor(Math.random() * phrases.length);

$(() => {
    const appUrl = "https://thor-converter-be.onrender.com/"
    // const appUrl = "http://127.0.0.1:5000/"
    const handleInitialLoadError = () => {
        $('#overlay').fadeOut();
        $('#submit-button').prop("disabled", true);
        $('#submit-button').text("Error: Disabled");
        let errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">Error: Server offline.</p> <p class="text-white-50 mx-auto mt-2 mb-2">Please try again in 5 minutes</p>`;
        $('#errors').append(errorHTML);
    }
    // Initial load function.
    // Checks if the backend is up and running.
    // Displays an error if it is not.
    $.ajax({
        url: appUrl,
        type: 'GET',
        cache: false,
        contentType: false,
        processData: false,
        tryCount: 0,
        retryLimit: 3,
        success: () => {
            $('#submit-button').text(phrases[phraseIndex])
            $('#overlay').fadeOut()
        },
        error: (xhr, textStatus, errorThrown) => {
            if (textStatus == 'timeout') {
                this.tryCount++;
                if (this.tryCount <= this.retryLimit) {
                    setTimeout(() => {$.ajax(this)},1000)
                    $.ajax(this);
                    return;
                }
                handleInitialLoadError()
                return;
            }
            if (xhr.status == 500) {
                handleInitialLoadError()
            } else {
                handleInitialLoadError()
            };
        }
    });

    // Sets the select to have the current supported clients/vms'
    $.each(client_list, function (key, value) {
        $('#client_select')
            .append($("<option></option>")
                .attr("value", key)
                .text(value));
    });

    //Form submission handler
    $('form').on('submit', (e) => {
        e.preventDefault();
        if ($('#errors').children().length > 0) {
            $('#errors').children().remove();
        };

        let throgressContainer = document.getElementById("throgress");

        let throgImg = document.createElement("img");
        throgImg.setAttribute("src", "static/assets/img/throg.png");
        throgImg.setAttribute("id", "throg");
        throgImg.setAttribute("alt", "In Throgress");
        throgImg.setAttribute("class", "rotate");

        let inThrogress = document.createElement("p");
        inThrogress.setAttribute("id", "loading");
        inThrogress.setAttribute("class", "text-white-50 mx-auto mt-2 mb-3");
        inThrogress.textContent = "In Throgress...";

        throgressContainer.append(throgImg);
        throgressContainer.append(inThrogress);

        const removeThrog = () => {
            throgImg.remove();
            inThrogress.remove();
            
        };

        let formData = new FormData();
        let client = (document.getElementById('client_select'));
        let upload = document.querySelector('#convert_files');
        let url = appUrl
        for (let f of upload.files) {
            formData.append("file", f);
        };
        formData.append("client", client.options[client.selectedIndex].text);

        let req = new XMLHttpRequest();

        // Error Handler
        req.onreadystatechange = (ev) => {
            if (req.readyState === 4) {
                if (req.status !== 200) {
                    if (req.status === 0){
                        req.abort();
                        let errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">Error: Server offline.</p> <p class="text-white-50 mx-auto mt-2 mb-2">Please try again in 5 minutes</p>`;
                        $('#errors').append(errorHTML);
                        removeThrog();
                        return;
                    }
                    req.abort();
                    let errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">Error: Please check your files.</p>`;
                    $('#errors').append(errorHTML);
                    removeThrog();
                    return;
                };
            };
        };

        if (upload.files.length < 1) {
            req.abort();
            let errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">Error: No file uploaded.</p>`;
            $('#errors').append(errorHTML);
            removeThrog();
            return
        } else if (upload.files.length > 1) {
            req.open('POST', url);
            req.responseType = 'blob';
            req.contentType = "application/zip";
            req.onload = (e) => {
                let contentDispo = e.currentTarget.getResponseHeader('Content-Disposition');
                let blob = new Blob([e.currentTarget.response], { type: 'application/zip' });
                let fileName = contentDispo.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)[1];
                let a = document.createElement('a');
                let dlurl = window.URL.createObjectURL(blob);
                a.setAttribute('download', fileName);
                a.setAttribute("href", dlurl);
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(dlurl);
                removeThrog();
            }
            req.send(formData);
        } else {
            req.open('POST', url);
            req.responseType = 'blob';
            req.contentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
            req.onload = (e) => {
                let contentDispo = e.currentTarget.getResponseHeader('Content-Disposition');
                let blob = new Blob([e.currentTarget.response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                let fileName = contentDispo.slice(22, contentDispo.length - 1);
                let a = document.createElement('a');
                let dlurl = window.URL.createObjectURL(blob);

                a.setAttribute('download', fileName.trim());
                a.setAttribute("href", dlurl);
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(dlurl);
                removeThrog();

            }
            req.send(formData);
        };
    });
});