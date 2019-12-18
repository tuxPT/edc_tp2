let map = L.map('mapid').setView([40, -8], 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiY2F0YXJpbmFzaWx2YSIsImEiOiJjazF1dHAwNmgxMXhuM29udTAyMGU4c3dnIn0.xskWNOn6ZoSHGU6i7UGyEA', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibWFyaW9scGFudHVuZXMiLCJhIjoiY2syYzhkcjdpMHpxbzNibWpjN3F2aDU3dyJ9.FklIUy73dB7yzL7NSYLvWA'
}).addTo(map);

L.control.scale().addTo(map);

let layerGroup = L.layerGroup().addTo(map);

map.on("moveend", function () {
    let zoom = map.getZoom();
    let c = map.getCenter();
    console.log('Zoom level: ' + zoom);
    let radius = 0;
    if (zoom <= 7) {
        radius = 560;
    } else if (zoom >= 17) {
        radius = 5;
    } else {
        radius = (-111 / 2) * zoom + (1897 / 2);
    }
    let url = 'listar_incidentes_map?lat=' + c.lat + '&lng=' + c.lng + '&radius=' + radius;
    fetch(url).then(res => res.json()).then((out) => {
        layerGroup.clearLayers();
        console.log(out.length);
        for (let i = 0; i < out.length; i++) {
            let lat = out[i]["Latitude"];
            let lng = out[i]["Longitude"];
            let marker = L.marker([lat, lng]);
            marker.bindPopup(out[i]['Natureza']);
            layerGroup.addLayer(marker);
        }
    }).catch(err => {
        throw err
    });
});

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
        lat = position.coords.latitude;
        lng = position.coords.longitude;
        var newLatLng = new L.LatLng(lat, lng);
        map.panTo(newLatLng);
    });
}