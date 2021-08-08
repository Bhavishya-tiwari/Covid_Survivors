

//***********************************Global variables******************************** */
var data_inc
var data_map
var covid_data;
var state_name;
var Country_data;
var dist_data;
var selected_country;
var state_selected;
var dist_name;
var is_notstate = false;
var All_countries
var vaccD

//*********************************Api section********************************************** 



fetch('https://api.covid19india.org/data.json')
    .then(response => response.json())
    .then(data => {

        let latestCases = data.cases_time_series[(data.cases_time_series).length - 1]
        let V = data.tested[(data.tested).length - 1]


        vaccD = {
            "dc": latestCases.dailyconfirmed,
            "dd": latestCases.dailydeceased,
            "dr": latestCases.dailyrecovered,
            "v": V.totalindividualsvaccinated,
            "tc": latestCases.totalconfirmed,
            "td": latestCases.totaldeceased,
            "tr": latestCases.totalrecovered,

        }
    })


fetch('https://corona.lmao.ninja/v2/jhucsse')
    .then(response => response.json())
    .then(data => {
        mapboxgl.accessToken = 'pk.eyJ1IjoiYmhhdmlzaHlhdDI0IiwiYSI6ImNrcmFlbXV2azRmanAyb3FobWtyYXI2dWwifQ.wfb9sjo6qtn43ZqcEBA9BQ';
        var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [78.289633, 23.541513],
            zoom: 10
        });



        fetch('https://corona.lmao.ninja/v2/countries?yesterday&sort')
            .then(response => response.json())
            .then(data => {
                let index = 0;
                var cntry = "<option selected>Country</option>"
                data.forEach(e => {
                    cntry = cntry + `<option value="${index}" >${e.country}</option>`
                });
                document.getElementById("country").innerHTML = cntry
                data.forEach(e => {
                    latitude = e.countryInfo.lat;
                    longitude = e.countryInfo.long;

                    cases = e.deaths;
                    if (cases / 100000 > 255) {
                        color = "rgb(255, 100, 0)";
                    }
                    else {
                        color = `rgb(${cases / 1000}, 0, 100)`;
                    }
                    // Mark on the map
                    new mapboxgl.Marker({
                        draggable: false,
                        color: color
                    }).setLngLat([longitude, latitude])
                        .addTo(map);
                });
                All_countries = data
            })




        document.getElementById("DataShown").addEventListener('click', function () {
            $('#CS').remove(); // this is my <canvas> element
            $('#SD').remove(); // this is my <canvas> element
            $('#ff').append(` <div id="CS">

                            
            <canvas id="myChartCS" style="width:100%;max-width:600px"></canvas>
     </div>
     <div id="SD">

            
            <canvas id="myChartSD" style="width:100%;max-width:600px"></canvas>
     </div>`);
            if (selected_country == "India") {

                
                var loc = 0;
                
                // getting location of that state
                data_map.forEach(e => {
                    if (e.province == state_name) {
                        loc = e.coordinates;
                        var c = e.stats.confirmed
                        var xValues = ["Confirmed", "Deaths", "Recovered"];
                        var yValues = [c, e.stats.deaths, e.stats.recovered];
                        var barColors = ["white", "red", "blue"];

                        new Chart("myChartCS", {
                            type: "bar",
                            data: {
                                labels: xValues,
                                datasets: [{
                                    backgroundColor: barColors,
                                    data: yValues
                                }]
                            },
                            options: {
                                indexAxis: 'y',
                                legend: { display: false },
                                title: {
                                    display: true,
                                    text: e.province
                                }
                            }
                        });
                    }
                });
                let district_full_data = dist_data[state_selected]["districtData"][dist_name]
                var xValues = [`Confirmed (${district_full_data.confirmed})`, "Deaths", "Recovered", "Active"];
                var yValues = [district_full_data.confirmed, district_full_data.deceased, district_full_data.recovered, district_full_data.active];
                var barColors = ["white", "red", "blue", "pink"];
                
                new Chart("myChartSD", {
                    type: "bar",
                    data: {
                        labels: xValues,
                        datasets: [{
                            backgroundColor: barColors,
                            data: yValues
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        legend: { display: false },
                        title: {
                            display: true,
                            text: dist_name
                        }
                    }
                });
      









        map.flyTo({

            center: [loc.longitude, loc.latitude],
            essential: true // this animation is considered essential with respect to prefers-reduced-motion
        });
    }





            else if (is_notstate == false) {






    var loc = 0;



    All_countries.forEach(e => {
        if (e.country == selected_country) {
            document.getElementById('flag').innerHTML = `<img class="flagimg" src="${e.countryInfo.flag}" alt="${e.country}"></img>`

            var xValues = ["Active", "Cases", "Deaths", "Recovered"];
            var yValues = [e.active, e.cases, e.deaths, e.recovered];
            var barColors = ["white", "purple", "red", "blue"];

            new Chart("myChartCS", {
                type: "bar",
                data: {
                    labels: xValues,
                    datasets: [{
                        backgroundColor: barColors,
                        data: yValues
                    }]
                },
                options: {
                    indexAxis: 'y',
                    legend: { display: false },
                    title: {
                        display: true,
                        text: e.country
                    }
                }
            });
        }
    })


    data_map.forEach(e => {
        if (e.province == state_selected) {
            loc = e.coordinates;


            var c = e.stats.confirmed
            var xValues = ["Confirmed", "Deaths", "Recovered"];
            var yValues = [c, e.stats.deaths, e.stats.recovered];
            var barColors = ["white", "red", "blue"];

            new Chart("myChartSD", {
                type: "bar",
                data: {
                    labels: xValues,
                    datasets: [{
                        backgroundColor: barColors,
                        data: yValues
                    }]
                },
                options: {
                    indexAxis: 'y',
                    legend: { display: false },
                    title: {
                        display: true,
                        text: e.province
                    }
                }
            });



        }
    });






    map.flyTo({
        center: [loc.longitude, loc.latitude],
        essential: true // this animation is considered essential with respect to prefers-reduced-motion
    });




}
else if (is_notstate) {
    var loc = 0;
    All_countries.forEach(e => {
        if (e.country == selected_country) {

            var xValues = ["Active", "Cases", "Deaths", "Recovered"];
            var yValues = [e.active, e.cases, e.deaths, e.recovered];
            var barColors = ["white", "purple", "red", "blue"];

            new Chart("myChartCS", {
                type: "bar",
                data: {
                    labels: xValues,
                    datasets: [{
                        backgroundColor: barColors,
                        data: yValues
                    }]
                },
                options: {
                    indexAxis: 'y',
                    legend: { display: false },
                    title: {
                        display: true,
                        text: e.country
                    }
                }
            });





            document.getElementById('flag').innerHTML = `<img class="flagimg" src="${e.countryInfo.flag}" alt="${e.country}"></img>`

            map.flyTo({
                center: [e.countryInfo.long, e.countryInfo.lat],
                essential: true // this animation is considered essential with respect to prefers-reduced-motion
            });
        }
    });
}
        });

map.addControl(
    new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl
    })
);

//*******************************************************************************
// filling data
var map_data_arr = []
data.forEach(e => {
    var obj = {
        'type': 'Feature',
        'properties': {
            'description': ` <div id="pop"> <p>country : ${e.country}</p>
                                   <p>confirmed : ${e.stats.confirmed}</p>
                                   <p>deaths : ${e.stats.deaths}</p>
                                   <p>recovered :${e.stats.recovered} op</p>
                                   <p>province : ${e.province}</p> </div>`
        },
        'geometry': {
            'type': 'Point',
            'coordinates': [e.coordinates.longitude, e.coordinates.latitude]
        }
    }
    map_data_arr.push(obj)
});
//******************************************************************************************************************
map.on('load', function () {
    map.addSource('places', {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': map_data_arr
        }
    });

    map.addLayer({
        'id': 'places',
        'type': 'circle',
        'source': 'places',
        'paint': {
            'circle-color': "red",
            'circle-radius': 5,
            'circle-stroke-width': 2,
            'circle-stroke-color': 'white'
        }
    });
    // Create a popup, but don't add it to the map yet.
    var popup = new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: false
    });

    map.on('mouseenter', 'places', function (e) {
        map.getCanvas().style.cursor = 'pointer';

        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties.description;


        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        // Populate the popup and set its coordinates
        // based on the feature found.
        popup.setLngLat(coordinates).setHTML(description).addTo(map);
    });

    map.on('mouseleave', 'places', function () {
        map.getCanvas().style.cursor = '';
        popup.remove();
    });
});
data_map = data
    })
fetch('https://api.covid19india.org/state_district_wise.json')
    .then(response => response.json())
    .then(data => {
        dist_data = data
    })







//**********************************Functions******************************************
function myFunction2(e) {

    var index = 0;
    var options = "<option selected>State</option>"
    var selectedValues = [].filter
        .call(document.getElementById("country").options, option => option.selected)
        .map(option => option.text);

    selected_country = selectedValues
    data_map.forEach(e => {
        if (e.country == selectedValues) {
            if (e.province != null) {

                if (index == 0) {
                    document.getElementById("state").removeAttribute("disabled");
                }
                options = options + `<option value="${index}">${e.province}</option>`
                index++;
                is_notstate = false;
            }
            else {
                document.getElementById("state").setAttribute("disabled", false);
                document.getElementById("dist").setAttribute("disabled", false);

                is_notstate = true;
            }
        }
    });
    document.getElementById("state").innerHTML = options;
}

function myFunction(e) {  // on state selection
    if (selected_country == "India") {
        var options2 = "<option selected>District</option>"
        var selectedValues = [].filter
            .call(document.getElementById("state").options, option => option.selected)
            .map(option => option.text);
        state_selected = selectedValues[0]
        document.getElementById("dist").removeAttribute("disabled");
        let districts = dist_data[selectedValues[0]].districtData
        let index = 0
        for (district in districts) {
            options2 = options2 + `<option value="${index}">${district}</option>`
            index++;
        }
        document.getElementById("dist").innerHTML = options2;
        state_name = selectedValues[0]
    }
    else {
        var selectedValues = [].filter
            .call(document.getElementById("state").options, option => option.selected)
            .map(option => option.text);
        document.getElementById("dist").setAttribute("disabled", false);
        state_selected = selectedValues[0]
    }
};

function myFunction1(e) {
    selectedValuesd = [].filter
        .call(document.getElementById("dist").options, option => option.selected)
        .map(option => option.text);
    covid_data = dist_data[state_selected]["districtData"][selectedValuesd[0]]
    dist_name = selectedValuesd[0]
}


// *******************Vaccinated Data***************************************

var widthhh;
function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}



var iii = 0;
window.addEventListener('scroll', function () {
   
    if (iii == 0) {
        if(widthhh<800){
            if (window.pageYOffset > 720) {

                animateValue(document.getElementById('dcc'), parseInt(vaccD.dc * 3 / 4), parseInt(vaccD.dc), 4000);
                animateValue(document.getElementById('ddd'), parseInt(vaccD.dd * 3 / 4), parseInt(vaccD.dd), 4000);
                animateValue(document.getElementById('drr'), parseInt(vaccD.dr * 3 / 4), parseInt(vaccD.dr), 4000);
                animateValue(document.getElementById('vv'), parseInt(vaccD.v * 3 / 4), parseInt(vaccD.v), 4000);
                animateValue(document.getElementById('tcc'), parseInt(vaccD.tc * 3 / 4), parseInt(vaccD.tc), 4000);
                animateValue(document.getElementById('tdd'), parseInt(vaccD.td * 3 / 4), parseInt(vaccD.td), 4000);
                animateValue(document.getElementById('trr'), parseInt(vaccD.tr * 3 / 4), parseInt(vaccD.tr), 4000);
    
    
                iii = 2;

        }}
        if(widthhh<383){
            if (window.pageYOffset >496 ) {

                animateValue(document.getElementById('dcc'), parseInt(vaccD.dc * 3 / 4), parseInt(vaccD.dc), 4000);
                animateValue(document.getElementById('ddd'), parseInt(vaccD.dd * 3 / 4), parseInt(vaccD.dd), 4000);
                animateValue(document.getElementById('drr'), parseInt(vaccD.dr * 3 / 4), parseInt(vaccD.dr), 4000);
                animateValue(document.getElementById('vv'), parseInt(vaccD.v * 3 / 4), parseInt(vaccD.v), 4000);
                animateValue(document.getElementById('tcc'), parseInt(vaccD.tc * 3 / 4), parseInt(vaccD.tc), 4000);
                animateValue(document.getElementById('tdd'), parseInt(vaccD.td * 3 / 4), parseInt(vaccD.td), 4000);
                animateValue(document.getElementById('trr'), parseInt(vaccD.tr * 3 / 4), parseInt(vaccD.tr), 4000);
    
    
                iii = 2;

        }}
        else{
        if (window.pageYOffset > 220) {

            animateValue(document.getElementById('dcc'), parseInt(vaccD.dc * 3 / 4), parseInt(vaccD.dc), 4000);
            animateValue(document.getElementById('ddd'), parseInt(vaccD.dd * 3 / 4), parseInt(vaccD.dd), 4000);
            animateValue(document.getElementById('drr'), parseInt(vaccD.dr * 3 / 4), parseInt(vaccD.dr), 4000);
            animateValue(document.getElementById('vv'), parseInt(vaccD.v * 3 / 4), parseInt(vaccD.v), 4000);
            animateValue(document.getElementById('tcc'), parseInt(vaccD.tc * 3 / 4), parseInt(vaccD.tc), 4000);
            animateValue(document.getElementById('tdd'), parseInt(vaccD.td * 3 / 4), parseInt(vaccD.td), 4000);
            animateValue(document.getElementById('trr'), parseInt(vaccD.tr * 3 / 4), parseInt(vaccD.tr), 4000);


            iii = 2;
        }}
    }


});

widthhh =  screen.width

window.addEventListener('resize',()=>{

  widthhh =  screen.width

})

