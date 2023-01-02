# Set up and Run

For local work environment, run these commands then you can send request to api.
```
python -m venv env
```
```
source env/bin/activate
```
```
pip install -r requirements.txt
```
```
python manage.py migrate
```
```
python manage.py runserver
```

# For Running Unit Tests

```
python manage.py test
```
Code covarage document is under the cover folder. It can be open index.html to view the detail of test document. The file that contain api codes views.py covarage is 84%.
# Build for Docker
```
docker login --username username
```
```
docker-compose up -d
```

