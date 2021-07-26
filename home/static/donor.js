console.log("Donor wala js");
bg = document.getElementById("bgrp")
// console.log(bg);
var bg;

$('#Donor_search').submit(function (event) {
    var getValue = document.getElementById('bgrp').selectedOptions[0].value;
    $('#showdata').empty();
    var formData = {
        'Blood_grp_val': getValue,

        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    };
    $.ajax({
        type: 'POST',
        url: '/donors',
        data: formData,
        encode: true
    })
        .done(function (data) {
            var st = ""
            console.log("idovm");
            updates = JSON.parse(data);
            console.log(data)

            updates.forEach(e => {
                st = st + `<div class="card m-3 cd" style="width: 18rem;">
                <div class="card-body">
                     <h5 class="card-title">Name : ${e.name}</h5>
                     <h6 class="card-subtitle mb-2 text-muted">Email : ${e.email}</h6>
                     <h6 class="card-text">Hospital name: ${e.Hospital_name} <br>
                     Hospital email : ${e.Hospital_email}<br>
            
    
                </div>
           </div>`



            });
            document.getElementById('showdata').innerHTML = st;

        });
    event.preventDefault();
    // console.log(formData);
});
