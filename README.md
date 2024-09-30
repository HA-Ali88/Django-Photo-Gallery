# Photo Gallery Website
A fully featured photo gallery web application with authentication, image uploading, and user interaction features such as liking and bookmarking images. It also includes functionalities for ranking images by popularity, viewing a list of users, and more. Built using Django 4.2, JavaScript, with Redis to store image views and likes.
Features
- User Authentication: 
  - Register new users
  - Social authentication using Facebook, Twitter, and Google
  - Login/Logout functionality
  - Password change and reset
   - Edit profile

- User Management:
  - View a list of users
  - View individual user profiles
  - Follow users

- Image Management:
  - Upload images
  - View a list of images
  - View image details
  - Bookmark images
  - Like images
  - Rank images by the number of views

- Backend:
  - Use Redis for caching image likes and views for ranking

Tech Stack
- Frontend: JavaScript, HTML, CSS
- Backend: Python, Django 
- Database: SQLite 
- Caching: Redis
- Authentication: Django Authentication

Getting Started
Prerequisites
- Python 3.2

Installation
1. Clone the repository:
bash
   git clone https://github.com/ HA-Ali88/Django-Photo-Gallery.git
   cd Django-Photo-Gallery

2. Install backend dependencies:
   pip install -r requirements.txt

3. Set up Redis:
   - Install Redis on your system. Follow the instructions at Redis installation guide (https://redis.io/docs/getting-started/installation/).

4. Set up the database:
   python manage.py migrate

5. Run the development server:
   python manage.py runserver

6. Access the site at `http://localhost:8000/account/`.
Environment Variables
To enable social authentication in Django using Facebook, Twitter, and Google, configure the following in your settings.py file. These settings use social-auth-app-django for social authentication:
# Facebook OAuth
SOCIAL_AUTH_FACEBOOK_KEY = 'XXX'  # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'XXX'  # Facebook App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']  # Permissions requested from Facebook
# Twitter OAuth
SOCIAL_AUTH_TWITTER_KEY = 'XXX'  # Twitter API Key
SOCIAL_AUTH_TWITTER_SECRET = 'XXX'  # Twitter API Secret
# Google OAuth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'XXX'  # Google Client ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'XXX'  # Google Client Secret
Replace 'XXX' with your actual App ID, API Key, Client ID, and Secret for each respective platform.

Redis Setup for Image Views and Likes
Image views and likes are stored in Redis for fast ranking and retrieval.
- Views: Every time an image is viewed, a Redis key is incremented.
- Likes: When a user likes an image, it is stored in Redis, and the like count is updated.

Endpoints
- /account/ – Get the dashboard. 
- /admin/ – Get the admin page.
After logging into the dashboard, you can navigate to other pages using the navigation bar.

Frontend Features
- Image Uploading: Upload images using JavaScript.
- Bookmarking: Users can bookmark their favorite images from other websites to upload to this site.
- Liking: Users can like images, and the like count is displayed in real-time.

Contribution
Feel free to open issues or contribute to this project by making a pull request. 

License
This project is licensed under the MIT License. See the LICENSE file for details.

