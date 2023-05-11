# Drf-Social
This is a simple social media backend project built using Django Rest Framework. The project features include following/unfollowing a profile, creating a post, deleting a created post, liking/disliking a post, commenting on a post, and viewing profile and post details.

## Getting Started
### Prerequisites
- docker-compose
### Installation
- Clone the repo

```
$ git clone git@github.com:sreehari/drf-social.git
$ cd drf-social
```

- Build the docker image

```
$ docker-compose build app
```

- Run the test to make sure everything is working fine

```
$ docker-compose run --rm app sh -c "python manage.py test"
```

- Run the server

```
$ docker-compose up
```

## API Endpoints
### Profile Endpoints
- `/api/profile/{id}/` (GET) Retrieve details of a profile by their ID
- `/api/profile/{id}/follow/` (POST) Follow a user by their ID
- `/api/profile/{id}/unfollow/` (POST) Unfollow a user by their ID

### Post Endpoints
- `/api/post/` (POST) Create a new post by providing the post content
- `/api/post/{id}/` (GET) Retrieve the details of a post by its ID
- `/api/post/{id}/` (DELETE) Delete a post by its ID
- `/api/post/{id}/like/` (POST) Like a post by its ID
- `/api/post/{id}/dislike/` (POST) Dislike a post by its ID

### Comment Endpoints
- `/api/comment/` (POST) Create a new post by providing post, post_id 
