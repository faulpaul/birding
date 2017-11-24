var  options = {
	'zoom': zoomset,
	'center': centerloc,
	'mapTypeID': google.maps.MapTypeId.ROADMAP
     };

var map = new google.maps.Map(document.getElementById("map"), options);
var markers = [];

for (var i = 0; i < locations.length; i++) {
	lat = locations[i][1];
	lng = locations[i][2];
	//if there is already a marker on the same position, change lat/lng randomly
	for (i=0; i < markers.length; i++) {
		var existingMarker = markers[i];
		var pos = existingMarker.getPosition();
		if (latlng.equals(pos)) {
			lat = lat + (Math.random() -.5) / 1500;
			lng = lng + (Math.random() -.5) / 1500;
		}
	}
	var latlng = new google.maps.LatLng(lat, lng);
        var marker = new google.maps.Marker({'position': latlng});
	google.maps.event.addListener(marker, 'click', (function(marker, i) {
        	return function() {
			var infowindow = new google.maps.InfoWindow();
			infowindow.setContent(locations[i][0]);
          		infowindow.open(map, marker);
		}
	})(marker, i));
	markers.push(marker);
      };

var markerCluster = new MarkerClusterer(map, markers, {imagePath: 'img/m', maxZoom: 10});
