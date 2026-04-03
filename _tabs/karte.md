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
    var latlngs = [];
    points.forEach(function(point) {
      var marker = L.marker([point.latitude, point.longitude]).addTo(map);
      marker.bindPopup(point.name);
      latlngs.push([point.latitude, point.longitude]);
    });

    if (latlngs.length >= 2) {
      L.polyline(latlngs, {
        color: 'grey',
        weight: 1.5,
        dashArray: '5, 5'
      }).addTo(map);

      map.fitBounds(L.latLngBounds(latlngs), { padding: [50, 50] });
    } else if (points.length === 1) {
      map.setView([points[0].latitude, points[0].longitude], 10);
    } else {
      map.setView([36.2048, 138.2529], 5); /* Default Japan */
    }
  })();
</script>
