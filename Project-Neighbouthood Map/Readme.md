# Single Page Application
  - This app presents a view of Lahore, Pakistan
  - 5 locations of Lahore are highlighted
 # Features
  - The app uses KnockoutJS to apply dynamic data bindings.
  - The app uses Google Maps to display a Map.
  -- The view is entirely implemented in index.html.
  - The app uses ajax to retrieve information from wikipedia about the locations. 
  - The app implements a list view along with a filter option. The filter   applied is based on 'type' of place. 'university', 'mall', 'hall', 'store', 'fastfood' are valid types.
  - The app animates markers based on clicks and checked checkboxes. 
  - The app uses the bootstrap framework to create a responsive web site.

# Run the App 
- You should have a valid internet connection so that the ajax data is retrieved along with a web browser. 
- Initiate a python web server locally at python -m http.server 8080 (python 3) and you can access the `index.html at localhost:8000/index.html`.
- You may run the app by just clicking on the `index.html` file.

# Code
- All data related operations ( Model ) are implemented in `data.js`.
- All controller related operations ( View Model ) are implemented in `controller.js`.
- `Index.html` contains the html and knockout data bindings required to implement the view.

# Acknoledgements
- I would like to thank Google Api references website for clearly explaining how to use their code. 
- I would also like to thank wikipedia for indicating how to run their code.
- I would also like to thank the author of the blog http://www.9bitstudios.com/ for helping me understand jsonp and how to just use a callback=? to resolve issues related to same-origin policy.


