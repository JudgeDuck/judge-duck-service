# Deployment

## Dependencies

* Python3
* Django >= 2
* markdown2 >= 2.3.5
* zip

## Configuration

* `server/pigeon-url.txt`: contains the url of judge-pigeon
* `server/jd_data/faq.md`: FAQ page content
* `server/jd_data/blogs/`
* `server/jd_data/code/`
* `server/jd_data/metadata/`
* `server/jd_data/pending/`
* `server/jd_data/pending_rejudge/`
* `server/jd_data/problems/`
* `server/jd_data/result/`
* `server/jd_data/temp/`
* `server/jd_data/users/`
* Django migration (**Please Ctrl-C the migration process when it stucks, since the judge thread started with the server would cause an infinity loop in background**)

## Running

```bash

cd server
mkdir -p jd_data/temp/
mkdir -p jd_data/problems/
mkdir -p jd_data/code/
mkdir -p jd_data/metadata/
mkdir -p jd_data/result/
mkdir -p jd_data/pending/
mkdir -p jd_data/pending_rejudge/
mkdir -p jd_data/users/
mkdir -p jd_data/blogs/
mkdir -p jd_data/problem_zips/
python3 manage.py runserver <ip>:<port>
```

