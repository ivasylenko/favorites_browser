To run Favorites Browser:

```
cat .env
DB_PASSWORD=xxxx
FLICKR_KEY=xxxx
DEBUG=true

docker-compose --env-file .env up
```

Sample feed query
```
http://127.0.0.1:5000/feed?text=Milky
```

Sample mark request:
```
curl --header "Content-Type: application/json"   --request POST   --data '{"id": 13, "title": "Eastern Pondhawk", "owner": "149638594@N05", "secret": "fba1c7cc32", "server": "2"}' http://127.0.0.1:5000/favorites
```

Sample query
```
http://127.0.0.1:5000/favorites?order_by=server&order=asc&page=2
```

Sample unmark
```
curl --request DELETE http://127.0.0.1:5000/favorites?id=51150451497
```