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
* Django migration

## Running

```bash
$ cd server
$ python3 manage.py runserver <ip>:<port>
```

