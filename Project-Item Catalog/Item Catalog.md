# Item Catalog

# Features
  - Website is hosted locally. You have to run this in the VM. 
  - Project implements CRUD
  - Project is developed using the Flask framework
  - Authentication is carried out using google-signin (Oauth v2)
  - A JSON endpoint is provided which can be checked at `"localhost:8000"/item/view/<id>/json`
  - Authorization and sessions are checked by Google authentication.
  - Page only assumes Admin and non-admin roles. Authenticated Users can edit, delete, create and view posts.
  - Unauthenticated Users can only view posts
  - The website uses postgresql as its primary database

# How To Use It
- use the command `psql` to run postgresql
- use the command `'create darabase cat'`. It is important to use the name `cat`.
- run the command `python database_setup.py` to setup the database.
- run the command `python database_insert.py` to populate the database. A sample user with an id of 1 has been added for testing purposes.
- run the command `python catalog.py` to run the server and access the website using `localhost:8000'

# Technical Aspects Of The Code
### Data Model
- The data model designed was a 1 to many relationship between a Category entity and a Items entity.
- The Category entity contains the columns: id, name
- The Items entity contains the columns: id, name, desc(description), user(unique google id) and category_id ( references Category.id )

### Modules
- Item Module implements a Flask blueprint and has functions for CRUD
- Category Module implements a Flask blueprint and has functions for CRUD
- Main Module contains error, and authentication functions and also creates the primary app






