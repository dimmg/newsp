# newsp

This is an illustration example of combining the async framework **Tornado** with async MongoDB driver **Motor** and 
**Elasticsearch** search engine.

The result presents a very simple and minimalistic restful API for creating news.

Features:
- Create news posts. See details about one or many post
- Paginated results
- Search posts
- Posts validation on creation
 

### Prerequisites

- docker-compose 1.11.2 or later


### Usage


#### Clone the repository

```
git clone https://github.com/dimmg/newsp.git
```

#### Build and run docker images

```
make start
```

#### Run application


SSH into the running `newsp` container and start the server 

```
docker exec -it newsp bash
python run.py
```

By having a running server, execute

```
docker inspect newsp
```

where `IPAddress` it is the address of the running application.

To access the API navigate to `http://{{IPAddress}}:5000`.


#### Endpoints

- `GET /news` - retrieve all posts
- `GET /news/<news_uuid>` - retrieve specific post
- `POST /news` - create post
- `GET /search` - search posts by subject and 

<br>

** _Note that this is a stub just for demonstration purposes. 
Many use cases have not been taken into consideration._