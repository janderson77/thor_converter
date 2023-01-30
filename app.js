const client_list = {
    "Clients": [
        {
            "id" : "1",
            "name" : "Papa Pita Bakery",
            "reg_markup" : "1.165",
            "ot_makrup" : "1.165",
            "dt_markup" : "1.165",
            "bonus_markup" : "1.165",
            "sources": ["Novatime", "masterfile"]
        },
        {
            "id": "2",
            "name": "PBM",
            "sources": ["Customer"]
        },
        {
            "id": "3",
            "name": "Novatime",
            "sources": ["Novatime"]
        },
        {
            "id" : "4",
            "name" : "Nutraceutical",
            "reg_markup" : "1.30",
            "ot_makrup" : "1.30",
            "dt_markup" : "1.30",
            "bonus_markup" : "1.30",
            "sources": ["Novatime"]
        },
        {
            "id": "5",
            "name": "Maximus",
            "sources": ["Customer"]
        }
    ]
}

const phrases = ["Crack the Sky", "Let Your Hammer Fly", "Call Down the Lightning",
"To Valhalla and Back", "Release Asgaard's Fury"]

$(() => {
    $('form').on('submit', (e) => {
        e.preventDefault();
    });
});