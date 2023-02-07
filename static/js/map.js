// center of the map
var center = [38.286, 35.681];

// Create the map
var map = L.map('map').setView(center, 9);

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

// Initialise the draw control and pass it the FeatureGroup of editable layers
var drawControl = new L.Control.Draw(drawPluginOptions);
map.addControl(drawControl);

var editableLayers = new L.FeatureGroup();
map.addLayer(editableLayers);
document.getElementsByClassName('leaflet-draw-draw-circlemarker')[0].style.display = 'none';
document.getElementsByClassName('leaflet-draw-draw-marker')[0].style.scale = '1.4';

// create a new div element
const newDiv = document.createElement("div");
let lang = window.location.href.split("/")[window.location.href.split("/").length - 1];

// and give it some content
const newContent = document.createTextNode(lang === "ar" ? "Konum Seç" : "Konum Seç");
newDiv.style.position = "absolute";
newDiv.style.right = "31px";
newDiv.style.width = "100px";
newDiv.style.backgroundColor = "rosybrown";

// add the text node to the newly created div
newDiv.appendChild(newContent);

// add the newly created element and its content into the DOM
const currentDiv = document.getElementsByClassName('leaflet-draw-draw-marker')[0];
currentDiv.appendChild(newDiv);

var button = document.createElement("Button");
button.innerHTML = '<i class="fa fa-language" style="font-size:24px"></i>';
button.style = "top:63px;right:5px;position:absolute;z-index: 9999"
button.onclick = function () {
    let lang = window.location.href.split("/")[window.location.href.split("/").length - 2];
    if (lang == "ar")
        window.location.href = "/tr/ihbar"
    else
        window.location.href = "/ar/ihbar"
};
document.body.appendChild(button);

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
