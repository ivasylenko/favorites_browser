To run Favorites Browser in docker compose:
```
cat .env
DB_PASSWORD=xxxx
FLICKR_KEY=xxxx
DEBUG=true

docker-compose --env-file .env up
```

Running tests:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt

PYTHONPATH=. pytest tests/test_resources.py
```

Sample queries:
```
curl http://127.0.0.1:5000/feed?text=Milky

curl --header "Content-Type: application/json"   --request POST   --data '{"id": 13, "title": "Eastern Pondhawk", "owner": "149638594@N05", "secret": "fba1c7cc32", "server": "2"}' http://127.0.0.1:5000/favorites

curl http://127.0.0.1:5000/favorites?order_by=server&order=asc&page=2

curl --request DELETE http://127.0.0.1:5000/favorites?id=51150451497
```