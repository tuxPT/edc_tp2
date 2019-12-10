var map = L.map('mapid').setView([40, -8], 12);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	maxZoom: 18,
	id: 'mapbox.streets',
	accessToken: 'pk.eyJ1IjoibWFyaW9scGFudHVuZXMiLCJhIjoiY2syYzhkcjdpMHpxbzNibWpjN3F2aDU3dyJ9.FklIUy73dB7yzL7NSYLvWA'
}).addTo(map);

var marker = L.marker([40, -8], { title: "Location", alt: "", draggable: true })
	.addTo(map).on('dragend', function () {
		var coord = String(marker.getLatLng()).split(',');
		var lat = parseFloat(coord[0].split('(')[1]);
		var lng = parseFloat(coord[1].split(')')[0]);
		document.getElementById('id_latitude').value = lat;
		document.getElementById('id_longitude').value = lng;
		reverse(lat, lng);
	});

document.getElementById('id_latitude').value = 40;
document.getElementById('id_longitude').value = -8;

if (navigator.geolocation) {
	navigator.geolocation.getCurrentPosition(function (position) {
		lat = position.coords.latitude;
		lng = position.coords.longitude;
		var newLatLng = new L.LatLng(lat, lng);
		marker.setLatLng(newLatLng);
		map.panTo(newLatLng);
		reverse(lat, lng);
		document.getElementById('id_latitude').value = lat;
		document.getElementById('id_longitude').value = lng;
	});
}

document.getElementById('id_latitude').oninput = function () {
	lat = document.getElementById('id_latitude').value;
	lng = document.getElementById('id_longitude').value;
	var newLatLng = new L.LatLng(lat, lng);
	marker.setLatLng(newLatLng);
	reverse(lat, lng);
};

document.getElementById('id_longitude').oninput = function () {
	lat = document.getElementById('id_latitude').value;
	lng = document.getElementById('id_longitude').value;
	var newLatLng = new L.LatLng(lat, lng);
	marker.setLatLng(newLatLng);
	reverse(lat, lng);
};

function reverse(lat, lng) {
	var url = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=' + lat + '&lon=' + lng;
	fetch(url).then(res => res.json()).then((out) => {
		var concelho = out['address']['county'];
		var distrito = concelho_2_distrito[concelho];
		
		var freguesia = ''
		if (('suburb' in out['address']) == true) {
			freguesia = out['address']['suburb'];
			
		} else if(('village' in out['address']) == true) {
			freguesia = out['address']['village'];
		}

		document.getElementById('id_distrito').value = distrito;
		document.getElementById('id_concelho').value = concelho;
		document.getElementById('id_freguesia').value = freguesia;
	}).catch(err => { throw err });
}