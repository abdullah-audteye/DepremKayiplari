// center of the map
var center = [38.286, 35.681];

// Create the map
var map = L.map('map').setView(center, 9);
var mcg = L.markerClusterGroup({
    chunkedLoading: true,
    //singleMarkerMode: true,
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

var selectedArray = [1, 2, 3, 4];
var selectedCountry = -1;

let values = {
    1: {status: "At Hospital", icon: greenIcon, color: "green"},
    2: {status: "Missing", icon: redIcon, color: "red"},
    3: {status: "Found", icon: yellowIcon, color: "yellow"},
    4: {status: "In Need of Help", icon: blueIcon, color: "blue"}
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
    fetch("api/kayiplar")
        .then((response) => response.json())
        .then((points) =>
            points.map((i) => {
                if (i.kayip_user.length < 0)
                    return;

                //illere göre filtrelemek için kontrol
                // let check = selectedCountry == -1 ? true : (i.ihbar_user.country == selectedCountry);

                var title = i.kayip_user[0]?.kayip_first_name + "-" + i.kayip_user[0]?.kayip_last_name + "-";
                var marker = L.marker(new L.LatLng(i.kayip_user[0]?.cordinate_x, i.kayip_user[0]?.cordinate_y), {
                    icon: values[i.kayip_user[0]?.kayip_status].icon,
                    title: title,
                });
                marker.bindPopup(
                    '<div class="row"><div class="col-12"><h3>Kayıp Bilgileri</h3></div><div class="col-12"><h5>isim:' +
                    " " +
                    i.kayip_user[0].kayip_first_name +
                    " " +
                    i.kayip_user[0].kayip_last_name +
                    '</h5></div><div class="col-12"><h5>Adres:' +
                    " " +
                    i.kayip_user[0].address + '</h5></div>' + '<div class="col-12"><h5>Durum:' +
                    " " +
                    values[i.kayip_user[0].kayip_status].status +

                    '</h5></div><div class="col-12"><h5>Detay:' +
                    " " +
                    i.kayip_user[0].detail +
                    '</h5></div><div style="border-top:1px solid gray;padding-top:5px;" class="col-12"><h4>İhbar Eden Bilgisi</h4>' +
                    '</div>' +
                    '<div class="col-12"><h6>isim:' +
                    " " +
                    i.ihbar_user.ihbar_first_name +
                    " " +
                    i.ihbar_user.ihbar_last_name +
                    '</h6></div>' +
                    '<div class="col-12"><h6>Telefon:' +
                    " " +
                    i.ihbar_user.phonenumber +
                    "</h6></div></div>",
                    {
                        maxWidth: 560,
                    }
                );

                if (selectedArray.includes(i.kayip_user[0].kayip_status))
                    mcg.addLayer(marker);
            })
        );
}

map.addLayer(mcg);

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
newDiv.style.right = "26px";
newDiv.style.width = "90px";
newDiv.style.height = "30px";
newDiv.style.borderRadius = "6px";
newDiv.style.fontWeight = "bold";
newDiv.style.backgroundColor = "rosybrown";

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
    addLayer();
}

function setSelectedCountry(id) {
    console.log(id, "id");

    var bounds = L.latLngBounds() // Instantiate LatLngBounds object
//35.529991,36.697083,36.719072,40.561523
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

    // var selectBox = document.getElementById("filterCountrySelect");
    // var selectedValue = selectBox.options[selectBox.selectedIndex].value;
    // selectedCountry = selectedValue;
}

generateLegend()

function generateLegend() {


    fetch("api/kayipstatus")
        .then((response) => response.json())
        .then((status) => {
            status.map((i) => {
                var txt1 = '<input onclick="setSelected(' + i.id + ')" type="checkbox" id="' + i.id + '" checked\n' +
                    '               style="accent-color: ' + values[i.id].color + ';" value="K">\n' +
                    '        <label for="' + i.id + '">' + i.name + '</label><br>';        // Create text with HTML

                $("#legendbar").append(txt1);   // Append new elements
            })
        });
}

map.on('draw:created', function (e) {
    var type = e.layerType,
        layer = e.layer;

    if (type === 'marker') {
        document.getElementById("cordinate_x").value = e.layer._latlng.lat;
        document.getElementById("cordinate_y").value = e.layer._latlng.lng;
        document.getElementById("openModal").click();
        // let lat = (e.layer._latlng.lat);
        // let lng = (e.layer._latlng.lng);
        // let str = '<button type="button" class="btn btn-info btn-lg" data-toggle="modal" data-target="#myModal">Fill Form</button>'
        // layer.bindPopup(str);
    }

    editableLayers.addLayer(layer);
});
