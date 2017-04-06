# A Multi-User Blog
- Website URL
-- https://udacity-158807.appspot.com/ 


# Features

  - Users can register and sign in!
  - Users can view/edit all of their associated posts.
  - The website remembers the User unless the user logs out.
  - Users can comment and like posts.
  - Users can edit comments

# How To Use It
- goto the website https://udacity-158807.appspot.com/
- If you have not registered as a user then please register otherwise you may sign in.
- The website will redirect to your main blog page which contains all of your blog posts. It will also contain a create post button for editing.
- You may edit your posts as well. 
- To go towards your main page, please visit the website again or press back.

# Technical Aspects Of The Code
### Data Model
- The data model designed was a 1 to many relationship between a User and a post.
- Four ndb.Model classes were created (Cookie, Post, User, Comments)
- The Cookie class contains association of a User key and a Cookie value.
- The Post class just contains the content of a Post alond with other Post attributes.
- The User class contains information about the user and implements a foreign key reference to the Post class.
- The Comments class contains information about the comments associated with a post.

### Code
- The code is divided into multiple files.
- main.py contains the main routing and handling information. 
- Modules have been created to handle actions on objects. Post handling is done by PostHandler.py module. Similarly, the CommentsHandler.py module contatins classes for handling comments related actions.
- helper.py provides methods and classes which are inherited in main.py.
- query.py provides methods for querying the database and returning the required result.
- database.py provides the databse models and their attributes.



