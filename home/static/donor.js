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
                st = st + `
                                <tr>
                                    <td>${e.Name}</td>
                                    <td>${e.Add}</td>
                                    <td>${e.Phone}</td>
                                    <td>Available</td>
                                </tr> `



            });

            newstr = `<table class="fl-table">
            <thead>
            <tr>
                <th class="head-table" >Hospital</th>
                <th class="head-table">Address</th>
                <th class="head-table">Contact no.</th>
                <th class="head-table">Status</th>
            </tr>
            </thead>
            <tbody>` + st + `  <tbody>
            </table>`
            document.getElementById('DataShown').innerHTML = newstr;
                


        });
    event.preventDefault();
    // console.log(formData);
});
