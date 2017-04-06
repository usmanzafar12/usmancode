var GoogleLocs = function(lat, lng, name, url, type) {
// this function defines a class that can be used to stored locations
        "use strict";
        var self = this;
        self.lat = lat;
        self.lng = lng;
        self.name = name;
        self.url = url;
        self.type = ko.observable(type);
};


function getData(webURL){
// this is the primary function to retrieve data from wikipedia
    "use strict";    
    var self = this;
    var completeURL = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&prop=text&rvsection=0&page='+ webURL + '&callback=?';
    $.ajax({
        type: "GET",
        url: completeURL,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data, textStatus, jqXHR){
            var message =  (data.parse) ? (data.parse.text["*"]) : ("no data is available");
            self.infoMessage =  message; 
        },
        error: function(jqXHR, status, err){
            self.infoMessage = "this physical site doesnt look famous." +
                                "wikipedia was empty";
        },
        complete: function(jqXHR, status){
            mapWindow.setContent(self.infoMessage);
            console.info("call finished");
            
        },

    });
}


var markerLocations = [new GoogleLocs(31.493370, 74.373201,
                      'A very fine store', 'Fine store', 'store'),
                       new GoogleLocs(31.492858, 74.372678,'Wedding Hall',
                        'noreen hall', 'hall'),
                       new GoogleLocs(31.493631, 74.375513,  'Lahore Broast',
                       'LaasDLASMDASOD', 'fastfood'),
                       new GoogleLocs(31.529414, 74.378658, 'Mall Of Lahore',
                       'Mall_of_Lahore', 'mall'),
                       new GoogleLocs(31.470561, 74.410431,
                      'Lahore University Of Managment And Sciences',
                      'Lahore_University_of_Management_Sciences', 'university')];




var AddMarker = function(loc) {
// This class defines a marker class along with additional methods
    "use strict";
    this.myLocation = new google.maps.LatLng(loc.lat, loc.lng);
    this.flag = ko.observable(true);
    this.infoMessage = 'Please wait, the content is loading';
    this.name = loc.name;
    console.info("This is from the addMarker", loc.type());
    this.type = loc.type();
    this.marker = new google.maps.Marker({
        position: this.myLocation,
        title: this.name,
    });    
    getData.call(this, loc.url);
    
};
