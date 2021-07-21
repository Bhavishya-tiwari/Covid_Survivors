<script>


       //***********************************Global variables******************************** */
       var data_inc
       var data_map
       var covid_data;
       var state_name;
       var Country_data;

       //*********************************Api section********************************************** 
       // var map_data_arr2 = []
       // fetch('https://corona.lmao.ninja/v2/countries?yesterday&sort')
       //        .then(response => response.json())
       //        .then(data => {
       //               data.forEach(e => {
       //                             // console.log(e);
       //                             var obj = {
       //                                    'type': 'Feature',
       //                             'properties': {
       //                                    'description': `  <p>country : ${e.country}</p>
       //                             <p>confirmed : ${e.cases}</p>
       //                             <p>deaths : ${e.recovered}</p>
       //                             <p>recovered :${e.deaths} op</p>
       //                             <p>province : ${e.active}</p> `
       //                      },
       //                             'geometry': {
       //                                    'type': 'Point',
       //                                    'coordinates': [e.countryInfo.long, e.countryInfo.lat]
       //                             }
       //                      }

       //                      map_data_arr2.push(obj)
       //               });
       //               // console.log(map_data_arr2);
       //                      Country_data = data;
       //        })
       fetch('https://api.covid19india.org/data.json')
              .then(response => response.json())
              .then(data => {
              })

       fetch('https://corona.lmao.ninja/v2/jhucsse')
              .then(response => response.json())
              .then(data => {
                     //  data.forEach(element => {
                     //         console.log(element.country);
                     //  });
                     console.log(typeof (data));
                     mapboxgl.accessToken = 'pk.eyJ1IjoiYmhhdmlzaHlhdDI0IiwiYSI6ImNrcmFlbXV2azRmanAyb3FobWtyYXI2dWwifQ.wfb9sjo6qtn43ZqcEBA9BQ';
                     var map = new mapboxgl.Map({
                            container: 'map',
                            style: 'mapbox://styles/mapbox/streets-v11',
                            center: [78.289633, 23.541513],

                            zoom: 10
                     });

                     var loc;
                     document.getElementById("DataShown").addEventListener('click', function () {
                            document.getElementById("Data_Box").innerHTML = `<b>${covid_data.confirmed}</b>`
                            // getting location of that state
                            data_map.forEach(e => {
                                   if (e.province == state_name) {
                                          loc = e.coordinates;
                                          // console.log(loc);

                                   }
                            });

                            map.flyTo({

                                   center: [loc.longitude, loc.latitude],
                                   essential: true // this animation is considered essential with respect to prefers-reduced-motion
                            });
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
                            // console.log(e);
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
                     // var map_data_arr2 = []
                     fetch('https://corona.lmao.ninja/v2/countries?yesterday&sort')
                            .then(response => response.json())
                            .then(data => {
                                   data.forEach(e => {
                                          // console.log(e);
                                         let long = String (e.countryInfo.long)
                                         let lat = String (e.countryInfo.lat)

                                          var obj = {
                                                 'type': 'Feature',
                                                 'properties': {
                                                        'description': `  <p>country : ${e.country}</p>
                                   <p>confirmed : ${e.cases}</p>
                                   <p>deaths : ${e.recovered}</p>
                                   <p>recovered :${e.deaths} op</p>
                                   <p>province : ${e.active}</p> `
                                                 },
                                                 'geometry': {
                                                        'type': 'Point',
                                          'coordinates': [long, lat]
                                                        
                                                 }
                                          }

                                          map_data_arr.push(obj)
                                   });
                                   console.log(map_data_arr);
                                   Country_data = data;
                            })


                
                     //******************************************************************************************************************
                     map.on('load', function () {
                            map.addSource('places', {
                                   'type': 'geojson',
                                   'data': {
                                          'type': 'FeatureCollection',
                                          'features':map_data_arr
                                          // [   {
                                          //        'type': 'Feature',
                                          //        'properties': {
                                          //               'description': `  <>`
                                          //        },
                                          //        'geometry': {
                                          //               'type': 'Point',
                                          // 'coordinates': [77, 20]
                                                        
                                          //        }
                                          // }]
                                   }
                            });
                            //*********

                            //************
                            map.addLayer({
                                   'id': 'places',
                                   'type': 'circle',
                                   'source': 'places',
                                   'paint': {

                                          'circle-color': "rgb(255, 24, 24)",
                                          'circle-radius': 6,
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
                                   // Change the cursor style as a UI indicator.
                                   map.getCanvas().style.cursor = 'pointer';

                                   var coordinates = e.features[0].geometry.coordinates.slice();
                                   var description = e.features[0].properties.description;

                                   // Ensure that if the map is zoomed out such that multiple
                                   // copies of the feature are visible, the popup appears
                                   // over the copy being pointed to.
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


                     console.log("sdnv");

              }
              )

       fetch('https://api.covid19india.org/state_district_wise.json')
              .then(response => response.json())
              .then(data => {
                     covidUpdate(data)
              })

       //**********************************Functions******************************************


       var options = "<option selected>State</option>"
       index = 0;
       var covidUpdate = function covidUpdate(data) {
              data_inc = data

              for (var stat in data) {
                     options = options + `<option value="${index}">${stat}</option>`
                     index++;

              }
              document.getElementById("state").innerHTML = options;

       }


       var state_selected;
       function myFunction(e) {  // on state selection
              var options2 = "<option selected>District</option>"
              var selectedValues = [].filter
                     .call(document.getElementById("state").options, option => option.selected)
                     .map(option => option.text);

              state_selected = selectedValues[0]

              document.getElementById("dist").removeAttribute("disabled");
              let districts = data_inc[selectedValues[0]].districtData
              let index = 0
              for (district in districts) {
                     options2 = options2 + `<option value="${index}">${district}</option>`
                     index++;
              }
              document.getElementById("dist").innerHTML = options2;
              state_name = selectedValues[0]
       };




       function myFunction1(e) {
              selectedValuesd = [].filter
                     .call(document.getElementById("dist").options, option => option.selected)
                     .map(option => option.text);
              covid_data = data_inc[state_selected]["districtData"][selectedValuesd[0]]
              dist_name = selectedValuesd[0]

       }


</script>