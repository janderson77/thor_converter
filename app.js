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
    });
});