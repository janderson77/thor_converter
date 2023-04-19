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
        let errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">Error: Server offline.</p> <p class="text-white-50 mx-auto mt-2 mb-2">Please try again in 2-3 minutes</p>`;
        $('#errors').append(errorHTML);
    }

    // Initial load function.
    // Checks if the backend is up and running.
    // Displays an error if it is not.
    const initialLoad = (tryCount=0) => {
        let retryLimit = 3;
        axios({
            url: appUrl,
            method: 'GET'
        }).then((e) => {
            $('#submit-button').text(phrases[phraseIndex]);
            $('#overlay').fadeOut();
        }).catch((e) => {
            tryCount++;
            if(tryCount <= retryLimit){
                setTimeout(() => {
                    initialLoad(tryCount++)
                }, 1000);
            }else{
                handleInitialLoadError();
            };
        });
    };
    initialLoad();

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

        if (upload.files.length < 1) {
            let errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">Error: No file uploaded.</p>`;
            $('#errors').append(errorHTML);
            removeThrog();
            return
        } else if (upload.files.length > 1) {
            axios({
                url: url,
                data: formData,
                headers: { "Content-Type": "multipart/form-data" },
                responseType: 'arraybuffer',
                method: 'POST',
            }).then((e) => {
                let contentDispo = e.headers['content-disposition']
                let blob = new Blob([e.data], { type: 'application/zip' });
                let fileName = contentDispo.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)[1];
                let a = document.createElement('a');
                let dlurl = window.URL.createObjectURL(blob);
                fileName = fileName.replace('"', '');
                fileName = fileName.replace('"', '');
                fileName = fileName.trim();
                a.setAttribute('download', fileName);
                a.setAttribute("href", dlurl);
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(dlurl);
                removeThrog();
            }).catch((e) => {
                const errorText = JSON.parse(new TextDecoder().decode(e.response.data))
                if(errorText.message === "undefined"){
                    errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">Unkown Error</p><p class="text-white-50 mx-auto mt-2 mb-2">Try opening the spreadsheet(s),</p> <p class="text-white-50 mx-auto mt-2 mb-2">save and close, and try again.</p><p class="text-white-50 mx-auto mt-2 mb-2">Or see administrator.</p>`;
                }else{
                    errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">${errorText.message}</p>`;
                }
                $('#errors').append(errorHTML);
                removeThrog();
                return;
            })
        } else {
            axios({
                method: 'POST',
                url: appUrl,
                data: formData,
                headers: { "Content-Type": "multipart/form-data", 'Accept': 'application/json' },
                responseType: 'arraybuffer',
            }).then((e) => {
                let contentDispo = e.headers['content-disposition']
                let blob = new Blob([e.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                let fileName = contentDispo.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)[1];
                let a = document.createElement('a');
                let dlurl = window.URL.createObjectURL(blob);
                fileName = fileName.replace('"', '');
                fileName = fileName.replace('"', '');
                fileName = fileName.trim();
                a.setAttribute('download', fileName);
                a.setAttribute("href", dlurl);
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(dlurl);
                removeThrog();
            }).catch((e) => {
                let errorHTML;
                const errorText = JSON.parse(new TextDecoder().decode(e.response.data))
                if(errorText.message === "undefined"){
                    errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">Unkown Error</p><p class="text-white-50 mx-auto mt-2 mb-2">Try opening the spreadsheet(s),</p> <p class="text-white-50 mx-auto mt-2 mb-2">save and close, and try again.</p><p class="text-white-50 mx-auto mt-2 mb-2">Or see administrator.</p>`;
                }else{
                    errorHTML = `<p class="text-white-50 mx-auto mt-2 mb-2">${errorText.message}</p>`;
                };
                $('#errors').append(errorHTML);
                removeThrog();
                return;
            })
        };
    });
});