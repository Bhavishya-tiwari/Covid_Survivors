

//***********************************Global variables******************************** */
var data_inc
var data_map
var covid_data;
var state_name;
var Country_data;
var dist_data;
var selected_country;
var is_notstate = false;
var All_countries

//*********************************Api section********************************************** 

fetch('https://api.covid19india.org/data.json')
    .then(response => response.json())
    .then(data => {
    })


fetch('https://corona.lmao.ninja/v2/jhucsse')
    .then(response => response.json())
    .then(data => {
        console.log(typeof (data));
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




        var loc = 0;
        document.getElementById("DataShown").addEventListener('click', function () {
            if (selected_country == "India") {
                // getting location of that state
                data_map.forEach(e => {
                    if (e.province == state_name) {
                        loc = e.coordinates;
                    }
                });
                document.getElementById("Data_Box").innerHTML = `<b>${covid_data.confirmed}</b>`
                map.flyTo({

                    center: [loc.longitude, loc.latitude],
                    essential: true // this animation is considered essential with respect to prefers-reduced-motion
                });
            }





            else if (is_notstate == false) {

                data_map.forEach(e => {
                    if (e.province == state_selected) {
                        loc = e.coordinates;


                    }
                });

                map.flyTo({
                    center: [loc.longitude, loc.latitude],
                    essential: true // this animation is considered essential with respect to prefers-reduced-motion
                });

            }
            else if (is_notstate) {
                All_countries.forEach(e => {
                    if (e.country == selected_country) {
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
                    'circle-color': "blue",
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
            }
            else {
                document.getElementById("state").setAttribute("disabled", false);
                is_notstate = true;
            }
        }
    });
    document.getElementById("state").innerHTML = options;
}

var state_selected;
function myFunction(e) {  // on state selection
    if (selected_country == "India") {
        var options2 = "<option selected>District</option>"
        var selectedValues = [].filter
            .call(document.getElementById("state").options, option => option.selected)
            .map(option => option.text);
        console.log(selectedValues);
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
        console.log(selectedValues);
        state_selected = selectedValues[0]
    }
};

function myFunction1(e) {
    selectedValuesd = [].filter
        .call(document.getElementById("dist").options, option => option.selected)
        .map(option => option.text);
    console.log(selectedValuesd);
    covid_data = dist_data[state_selected]["districtData"][selectedValuesd[0]]
    dist_name = selectedValuesd[0]
}
