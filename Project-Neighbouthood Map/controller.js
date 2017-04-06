var gmap = {
// this object provides options and methods for the gmap class
    map: null,
    initMap: function() {
        "use strict";
        google.maps.visualRefresh = true;
        var mapOptions = {
        center: new google.maps.LatLng(31.488309, 74.388875),
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var mapElement = document.getElementById('mapDiv');
    this.map = new google.maps.Map(mapElement, mapOptions);
    }
};

var setMarker = function(){
    "use strict";    
    var self = this;
    mapWindow.setContent(self.infoMessage);
    mapWindow.open(self.marker.get('map'), self.marker);    
    self.marker.setAnimation(google.maps.Animation.BOUNCE);
    window.setTimeout(function(){
        self.marker.setAnimation(null);
        console.info("hi");
    }, 1400);
};


var createMarkers = function(locs){
// This function creates the markers from the googleLocs class    
    "use strict";
    var markerArray = [];
    for(var i=0;i<locs.length;i++){
        var mark = new AddMarker(locs[i]);
        var self = mark;
        console.info(mark);
        mark.marker.setMap(gmap.map);
        mark.marker.addListener('click', (function(temp){
        return  function() {
                setMarker.call(temp);
            };
        }(mark)));

        markerArray.push(mark);
    }
    return markerArray;
};

var ViewModel = function(markers) {
    "use strict";
    this.markers = markers;
    this.locType = ko.observable();
    this.filteredItems = ko.computed(function() {
            var self = this;
        if(!self.locType()){
            this.markers.forEach(function (item){
                item.marker.setVisible(true);
            });
            return self.markers;
        } else {    
            return ko.utils.arrayFilter(this.markers, function(item) {
                if(item.type === self.locType().toLowerCase()){
                    item.marker.setVisible(true);
                    return true;
                } else {
                    item.marker.setVisible(false);
                    return false;
                }
            }, self);
        }
    
    }, this);            
};
    

var onGmapLoad = function () {
    "use strict";
    this.mapWindow = new google.maps.InfoWindow({
            content: self.infoMessage,
            maxWidth: 300
        });
    this.gmap.initMap();
    this.markers = createMarkers.call(this, markerLocations);
    this.view = new ViewModel(markers);
    ko.applyBindings(view);
    console.info("ASYNCHRONOUS!!!!!!!");
};


var mapError = function () {
  // Error handling

    "use strict";    
    console.info("error2");
    $("#mapDiv").text("There was an error loading google maps.");
};
