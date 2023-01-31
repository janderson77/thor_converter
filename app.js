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
            console.log(phraseIndex)
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
        let client = (document.querySelector('#client_select'))
        let upload = document.querySelector('#convert_files');
        for (let f of upload.files) {
            formData.append(client.options[client.selectedIndex].text, f)
        }

        $.ajax({
            url: 'http://127.0.0.1:5000/',
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
        }).done((res) => {
            console.log(res)
        })
    });
});