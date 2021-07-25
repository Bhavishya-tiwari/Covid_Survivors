
$('#msg_form').submit(function(event) {
    var msg =  document.getElementById("msg_send").value;;
    // $('#showdata').empty();
    console.log("coming");
    var formData = {
        'msg': msg,
       
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    };
    $.ajax({
            type: 'POST',
            url: '',
            data: formData,
            encode: true
        })
        .done(function(data) {
       
       
        });
    event.preventDefault();

});
var a = "{{request.user}}"
    console.log(a);


var g="";
setInterval(() => {
    
    fetch('/chatt')
    .then(response => response.json())
    .then(data => {
        str = ""
       data.forEach(e => {
        
           str = str + `NAme = ${e.name} , msg = ${e.msg} , username = ${e.un}`
           
    });
    document.getElementById('msgs').innerText = str
        
    })
},2000);
