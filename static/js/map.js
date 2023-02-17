// center of the map
var center = [38.286, 35.681];

// Create the map
var map = L.map('map').setView(center, 9);
var mcg = L.markerClusterGroup({
    chunkedLoading: true,
    //singleMarkerMode: true,
    disableClusteringAtZoom: 18,
    spiderfyOnMaxZoom: false,
});

var LeafIcon = L.Icon.extend({
    options: {
        iconSize: [24, 24],
        shadowSize: [50, 64],
        iconAnchor: [11, 94],
        shadowAnchor: [4, 62],
        popupAnchor: [0, -86],
    },
});
var greenIcon = new LeafIcon({iconUrl: "https://www.google.com/intl/en_us/mapfiles/ms/micons/green-dot.png",});
var redIcon = new LeafIcon({iconUrl: "https://www.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png",});
var yellowIcon = new LeafIcon({iconUrl: "https://www.google.com/intl/en_us/mapfiles/ms/micons/yellow-dot.png",});
var blueIcon = new LeafIcon({iconUrl: "https://www.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png",});
var purpleIcon = new LeafIcon({iconUrl: "https://www.google.com/intl/en_us/mapfiles/ms/micons/purple-dot.png",});
var orangeIcon = new LeafIcon({iconUrl: "https://www.google.com/intl/en_us/mapfiles/ms/micons/orange-dot.png",});

var selectedArray = [1, 2, 3, 4, 5];
var selectedCountry = -1;
var allData = [];

let values = {
    1: {status: "At Hospital", icon: greenIcon, color: "green"},
    2: {status: "Missing", icon: redIcon, color: "red"},
    3: {status: "Found", icon: yellowIcon, color: "yellow"},
    4: {status: "In Need of Help", icon: blueIcon, color: "blue"},
    5: {status: "Needs a Shelter", icon: purpleIcon, color: "purple"},
    6: {status: "Unknown", icon: orangeIcon, color: "orange"}
}

// Set up the OSM layer
L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18
    }).addTo(map);

// add a marker in the given location

// Initialise the FeatureGroup to store editable layers
var editableLayers = new L.FeatureGroup();
map.addLayer(editableLayers);

// define custom marker
var MyCustomMarker = L.Icon.extend({
    options: {
        shadowUrl: null,
        iconAnchor: new L.Point(12, 12),
        iconSize: new L.Point(24, 24),
        iconUrl: 'https://upload.wikimedia.org/wikipedia/commons/6/6b/Information_icon4_orange.svg'
    }
});

var drawPluginOptions = {
    position: 'topright',
    draw: {
        polyline: false,
        polygon: false,
        circle: false, // Turns off this drawing tool
        rectangle: false,
        marker: {
            icon: new MyCustomMarker()
        }
    },
    edit: false
};

////////////////////////////////////////////////////////////////////////
addLayer();

function addLayer() {
    mcg.clearLayers();
    map.removeLayer(mcg);
    fetch("api/kayiplar/all")
        .then((response) => response.json())
        .then((points) => {
                allData = points;
                points.map((i) => {
                    var marker = L.marker(new L.LatLng(i.cordinate_x, i.cordinate_y), {
                        icon: values[i.kayip_status]?.icon,
                    }).on('click', getMarkerData);
                    marker.bindPopup(
                        `<div id="popup_${i.id}"></div>`,
                        {
                            maxWidth: 560,
                        }
                    );

                    if (selectedArray.includes(i.kayip_status))
                        mcg.addLayer(marker);
                })
            }
        );

    map.addLayer(mcg);
}

function getMarkerData(e) {
    let id = $(e["target"]["_popup"]["_content"])[0].id.split('_')[1];
    fetch("api/kayiplar/" + id)
        .then((response) => response.json())
        .then((i) => {
            let val = '<div class="row"><div id="data-modal" class="col-12"><h3>Kayıp Bilgileri</h3></div><div class="col-12"><h5>isim:' +
                " " +
                (i.kayip_user[0].kayip_first_name) +
                " " +
                (i.kayip_user[0].kayip_last_name) +
                '</h5></div><div id="data-modal" class="col-12"><h5>Adres:' +
                " " +
                i.kayip_user[0].address + '</h5></div>' + '<div id="data-modal" class="col-12"><h5>Durum:' +
                " " +
                values[i.kayip_user[0].kayip_status]?.status +
                '</h5></div>' + '<div id="data-modal" class="col-12"><h5>Kişi Sayısı:' +
                " " +
                i.kayip_user.length +
                '</h5></div>' + '<div id="data-modal" class="col-12"><h5>Cinsiyet:' +
                " " +
                (i.kayip_user[0].gender == 'F' ? 'Kadın' : 'Erkek') +
                '</h5></div><div id="data-modal" class="col-12"><h5>Detay:' +
                " " +
                i.kayip_user[0].detail +
                '</h5></div><button style="margin:3px auto; width:130px; height:40px; border-radius:6px; background:#28a745; border:none; color:white; padding:10px;font-size:16px; text-align:center;"' +
                ' onclick="window.open(\'http://www.google.com/maps/place/' + i.kayip_user[0]?.cordinate_x + ',' + i.kayip_user[0]?.cordinate_y + '\' ,\'_blank\');">Konuma Git' +
                '</button><div style="border-top:1px solid gray;padding-top:5px;" class="col-12"><h4>İhbar Eden Bilgisi</h4>' +
                '</div>' +
                '<div id="data-modal" class="col-12"><h6>isim:' +
                " " +
                (i.ihbar_user.ihbar_first_name) +
                " " +
                (i.ihbar_user.ihbar_last_name) +
                '</h6></div>' +
                '<div class="col-12"><h6>Telefon:' +
                " " +
                (i.ihbar_user.phonenumber) +
                '</h6></div></div>';

            $('#popup_' + id).append(val);
        });
}

function addAsterixToString(value) {
    var result = value.split(" ", 2);
    return result.map((i) => {
        return i.split("").map((x, index) => {
            return index == 0 ? (x) : "*"
        }).join("")
    }).join(" ");
}

////////////////////////////////////////////////////////////////////////

// Initialise the draw control and pass it the FeatureGroup of editable layers
var drawControl = new L.Control.Draw(drawPluginOptions);
map.addControl(drawControl);

var editableLayers = new L.FeatureGroup();
map.addLayer(editableLayers);
document.getElementsByClassName('leaflet-draw-draw-circlemarker')[0].style.display = 'none';
document.getElementsByClassName('leaflet-draw-draw-marker')[0].style.scale = '1.4';

// create a new div element
let newDiv = document.createElement("div");

// and give it some content
const newContent = document.createTextNode("Konum Seç");
newDiv.style.position = "absolute";
newDiv.style.right = "0px";
newDiv.style.width = "113px";
newDiv.style.height = "33px";
newDiv.style.top = "1px";
newDiv.style.borderRadius = "4px";
newDiv.style.paddingLeft = "11px";
newDiv.style.fontWeight = "400";
newDiv.style.textAlign = "left";
newDiv.style.color = "white";
newDiv.style.zIndex = "-1";
newDiv.style.backgroundColor = "#da1e37";

// add the text node to the newly created div
newDiv.appendChild(newContent);

// add the newly created element and its content into the DOM
const currentDiv = document.getElementsByClassName('leaflet-draw-draw-marker')[0];
currentDiv.appendChild(newDiv);

function setSelected(id) {
    if (selectedArray.includes(id)) {
        const index = selectedArray.indexOf(id);
        if (index > -1) selectedArray.splice(index, 1);
    } else {
        selectedArray.push(id);
    }
    document.querySelector('#legendbar_content').querySelectorAll('input').forEach((btn) => {
        btn.disabled = true
    })
    addLayer();
    setTimeout(() => {
        document.querySelector('#legendbar_content').querySelectorAll('input').forEach((btn) => {
            btn.disabled = false
        })
    }, 1000)
}

function setSelectedCountry(id) {
    var polygonPoints = {
        2: [
            [36.07538422941732, 37.994225034592425],
            [36.18091040353196, 39.72534001336037],
            [34.540172959444554, 39.96051035009866],
            [34.93205872605833, 37.98116001588474]],
        1: [[38.21680877405232, 34.71204528737725],
            [38.09154169736558, 38.6341641679324],
            [36.50984563750561, 38.4583829295882],
            [36.558397114119714, 35.55249933321049]]
    };
    map.fitBounds(polygonPoints[id]);
}

function zoomToPoint(x, y, id) {
    if (x == null || y == null) {
        fetch("api/kayiplar/" + id)
            .then((response) => response.json())
            .then((obj) => {
                let vals = "";
                Object.keys(obj.kayip_user[0]).map((i, index) => {

                    if ((obj.kayip_user[0][i] == null || obj.kayip_user[0][i].length === 0))
                        return;
                    if (index == 1)
                        vals = vals + '<li style="list-style: none; color:white; text-align: center; border-bottom:1px solid black; cursor:pointer; padding: 4px; background-color: rgba(171,59,59,0.75)"' +
                            '>  <b> ' + (obj.kayip_user[0][i]) + ' ' + (obj.kayip_user[0][i]) + '  </b></li>'
                    else if (index > 2)
                        vals = vals + '<li style="list-style: none; color:white; border-bottom:1px solid black; cursor:pointer; padding: 4px; background-color: rgba(171,59,59,0.75)"' +
                            '>  <b>' + i + ' : </b>' + (obj.kayip_user[0][i]) + '</li>'
                })

                $('#search_results').empty();
                $('#search_results').append(vals);
                return;
            });
    } else {
        var bounds = L.latLngBounds()
        let lat_lng = [x, y]
        bounds.extend(lat_lng)
        map.fitBounds(bounds)
        $('#search_results').empty();
    }
}

generateLegend()

function toggleLegend() {
    document.getElementById('legendbar_content').style.display =
        document.getElementById('legendbar_content').style.display == "none" ? "block" : "none";
}

function clearSearch() {
    $('#search_results').empty();
    $('#example-search-input').val('');
}

function searchByName() {
    $('#search_results').empty();
    let userInput = document.getElementById('example-search-input').value;

    if (userInput.length < 3) {
        let resultListItem = '<li style="list-style: none; color:white; border-bottom:1px solid black; cursor:pointer; padding: 4px; background-color: rgba(61,84,131,0.75)">' +
            ' Must be At Least 3 Characters</li>';
        $('#search_results').append(resultListItem);
    }

    fetch("api/kayiplar/filter?first_name=" + userInput)
        .then((response) => response.json())
        .then((status) => {
            if (status.length == 0) {
                let resultListItem = '<li style="list-style: none; color:white; border-bottom:1px solid black; cursor:pointer; padding: 4px; background-color: rgba(61,84,131,0.75)">' + ' No Result</li>';
                $('#search_results').append(resultListItem);
            } else
                for (let i = 0; i < status.length; i++) {
                    console.log((status[i]), "12");
                    let resultListItem = i % 2 == 1 ? '<li style="list-style: none; color:white; border-bottom:1px solid black; cursor:pointer; padding: 4px; background-color: rgba(61,84,131,0.75)"' +
                        'onclick="zoomToPoint(' + status[i].cordinate_x + ',' + status[i].cordinate_y + ',' + status[i].id + ')">' + status[i].kayip_first_name + ' ' + status[i].kayip_last_name + '</li>'
                        :
                        '<li style="list-style: none; color:white; border-bottom:1px solid black; cursor:pointer; padding: 4px; ; background-color: rgba(89,120,190,0.75)"' +
                        'onclick="zoomToPoint(' + status[i].cordinate_x + ',' + status[i].cordinate_x + ',' + status[i].id + ')">' + status[i].kayip_first_name + ' ' + status[i].kayip_last_name + '</li>';
                    $('#search_results').append(resultListItem);
                }
        });
}

function generateLegend() {
    fetch("api/kayipstatus")
        .then((response) => response.json())
        .then((status) => {
            status.map((i) => {
                var txt1 = '<input onclick="setSelected(' + i.id + ')" type="checkbox" id="' + i.id + '" checked\n' +
                    '               style="accent-color: ' + values[i.id]?.color + ';" value="K">\n' +
                    '        <label for="' + i.id + '">' + i.name + '</label><br>';        // Create text with HTML

                $("#legendbar_content").append(txt1);   // Append new elements
            })
            $("#legendbar").append("<button id='legend_btn' style='position: absolute; width:50px; height:50px; margin-top:7px;background:#da1e37;border-radius:6px; border:none;box-shadow: 4px 4px 10px #adb5bd;' onclick='toggleLegend()'><i class='fa fa-filter text-white'></i></button>");
        });
}

map.on('draw:created', function (e) {
    var type = e.layerType,
        layer = e.layer;

    if (type === 'marker') {
        document.getElementById("cordinate_x").value = e.layer._latlng.lat;
        document.getElementById("cordinate_y").value = e.layer._latlng.lng;
        document.getElementById("openModal").click();
    }

    editableLayers.addLayer(layer);
});
