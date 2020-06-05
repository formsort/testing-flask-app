1. `pipenv install --dev`
2. `pipenv shell`
3. `vi $(pipenv --venv)/bin/activate` and append:

```
export FLASK_RUN_PORT=6000
export FLASK_DEBUG=1
```

4. `flask run`
