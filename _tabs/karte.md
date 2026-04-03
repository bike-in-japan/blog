---
title: Karte
icon: fas fa-map
order: 5
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

<div id="map" style="height: 600px; z-index: 1;"></div>

<script>
  (function() {
    var mapEl = document.getElementById('map');
    if (!mapEl || mapEl._leaflet_id) return;

    var points = [
      {% for point in site.data.geopoints %}
      {
        name: "{{ point.name }}",
        latitude: {{ point.latitude }},
        longitude: {{ point.longitude }}
      }{% unless forloop.last %},{% endunless %}
      {% endfor %}
    ];

    var map = L.map('map');

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    }).addTo(map);
    var greenIcon = new L.Icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });

    var latlngs = [];
    var japanLatLngs = [];
    points.forEach(function(point, index) {
      var isLast = (index === points.length - 1);
      var markerOptions = isLast ? { icon: greenIcon } : {};
      var marker = L.marker([point.latitude, point.longitude], markerOptions).addTo(map);
      marker.bindPopup(point.name);
      latlngs.push([point.latitude, point.longitude]);
      if (point.longitude > 125) {
        japanLatLngs.push([point.latitude, point.longitude]);
      }
    });

    if (japanLatLngs.length >= 2) {
      L.polyline(japanLatLngs, {
        color: 'grey',
        weight: 1.5,
        dashArray: '5, 5'
      }).addTo(map);
    }

    if (points.length >= 2) {
      var last2 = latlngs.slice(-2);
      map.fitBounds(L.latLngBounds(last2), { padding: [50, 50] });
    } else if (points.length === 1) {
      map.setView([points[0].latitude, points[0].longitude], 10);
    } else {
      map.setView([36.2048, 138.2529], 5); /* Default Japan */
    }
  })();
</script>
