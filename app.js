const client_list = {
        "Papa Pita Bakery": "Papa Pita Bakery",
        "PBM": "PBM",
        "Novatime": "Novatime",
        "Nutraceutical": "Nutraceutical",
        "Maximus": "Maximus"
}

const phrases = ["Crack the Sky", "Let Your Hammer Fly", "Call Down the Lightning",
"To Valhalla and Back", "Release Asgaard's Fury"]

$(() => {
    $.ajax({
        url: 'http://127.0.0.1:5000/',
        type: 'GET',
        cache: false,
        contentType: false,
        processData: false,
    }).done((data, textStatus, xhr) => {
        $('#overlay').fadeOut()
    })
    $.each(client_list, function(key, value) {   
        $('#client_select')
            .append($("<option></option>")
                       .attr("value", key)
                       .text(value)); 
   });

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