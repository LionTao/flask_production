# flask_production
production machine on web
Powered by Flask
Written in Python


## Rule Databse
Rules were written in database.txt
```angular2html
{facts} {facts} {results}
```
For example
(If) A (then) B
Then you should write
```angular2html
A B
```
in database.txt

## Develop
Dependencies:
```
jieba
flask
flask_bootstrap
flask_wtf
requests
```

TO run local test server
```bash
python app.py
```
Then    
- For forward production:visit [http://127.0.0.1:5000](http://127.0.0.1:5000)
- For backward production:visit [http://127.0.0.1:5000/reverse](http://127.0.0.1:5000/reverse)

## TODO
Modify database in Broswer
