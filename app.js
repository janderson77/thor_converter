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
    $.each(client_list, function(key, value) {   
        $('#client_select')
            .append($("<option></option>")
                       .attr("value", key)
                       .text(value)); 
   });

    $('form').on('submit', (e) => {
        e.preventDefault();
        // let data = [];

        // // Puts the selected client/vms as index 0 for the ajax request
        // data.push($('#client_select option:selected').text())

        // // Pushes the file or files to be uploaded to the data array for the ajax request
        // const uploadfiles = $('#convert_files')[0].files;
        // for (let el of uploadfiles) {
        //     data.push(el)
        // }

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