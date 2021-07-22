console.log("Donor wala js");
bg = document.getElementById("bgrp")
// console.log(bg);
var bg;











$('#Donor_search').submit(function(event) {
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
        .done(function(data) {
            updates = JSON.parse(data);
            console.log(updates)
            if (updates.length > 0 & updates != {}) {
            }
       
        });
    event.preventDefault();
    // console.log(formData);
});