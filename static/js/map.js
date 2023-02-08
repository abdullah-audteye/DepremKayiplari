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

////////////////////////////////////////////////////////////////////////

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
var greenIcon = new LeafIcon({
    iconUrl:
        "https://mt.googleapis.com/vt/icon/name=icons/onion/123-red-dot.png",
});

fetch("api/kayiplar")
    .then((response) => response.json())
    .then((points) =>
        points.map((i) => {
            var title = i.kayip_user[0].kayip_first_name + "-" + i.kayip_user[0].kayip_last_name + "-";
            var marker = L.marker(new L.LatLng(i.kayip_user[0].cordinate_x, i.kayip_user[0].cordinate_y), {
                icon: greenIcon,
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
                i.kayip_user[0].address +
                '</h5></div><div class="col-12"><h5>Detay:' +
                " " +
                i.kayip_user[0].detail +
                '</h5></div><div style="border-top:1px solid gray;padding-top:5px;" class="col-12"><h4>İhbar Eden Bilgisi</h4></div><div class="col-12"><h6>isim:' +
                " " +
                i.ihbar_user.ihbar_first_name +
                " " +
                i.ihbar_user.ihbar_last_name +
                '</h6></div><div class="col-12"><h6>Telefon:' +
                " " +
                i.ihbar_user.phonenumber +
                "</h6></div></div>",
                {
                    maxWidth: 560,
                }
            );
            mcg.addLayer(marker);
        })
    );
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
let lang = window.location.href.split("/")[window.location.href.split("/").length - 1].slice(0, 2);

// and give it some content
const newContent = document.createTextNode(lang === "ar" ? "حدد موقع المفقود" : "Konum Seç");
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
button.style = "top:63px;right:5px;position:absolute;z-index: 400"
button.onclick = function () {
    console.log("dil değiştirme");
};
document.body.appendChild(button);

newDiv = document.createElement("div");

// and give it some content
const newContents = document.createTextNode(lang === "ar" ? "Türkçe" : "عربي");
newDiv.style.position = "absolute";
newDiv.style.right = "36px";
newDiv.style.top = "0px";
newDiv.style.width = "100px";
newDiv.style.backgroundColor = "rosybrown";

// add the text node to the newly created div
newDiv.appendChild(newContents);
button.appendChild(newDiv);

button = document.createElement("Button");
button.innerHTML = '<i class="fa fa-info" style="font-size:24px"></i>';
button.style = "top:100px;right:5px;position:absolute;z-index: 400"
button.onclick = function () {
    $('#myMultiModal').modal('show');
};
document.body.appendChild(button);

newDiv = document.createElement("div");

// and give it some content
const newContentss = document.createTextNode(lang === "ar" ? "Bilgi Al" : "Bilgi Al");
newDiv.style.position = "absolute";
newDiv.style.right = "36px";
newDiv.style.top = "0px";
newDiv.style.width = "122px";
newDiv.style.backgroundColor = "rosybrown";

// add the text node to the newly created div
newDiv.appendChild(newContentss);
button.appendChild(newDiv);

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
