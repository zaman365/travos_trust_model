## Deploy

- All deploy-configs for daphne and nginx (and depricated gunicorn) are in ``_deploy-configs/``.

- Project is deployed at master branch via a CI gitlabrunner by ``.gitlab-ci.yml``.

- Password of the db user for the database is provided to ``settings.py`` at the deploy process via the script at ``/var/www/trustlab/dbkey.sh``.

- The deploy script is exchanging following strings in ``settings.py``:
  - DB NAME
  - DB USER
  - DB PASSWORD
  - STATIC URL & ROOT
  - MEDIA URL & ROOT

- Links for deploy \
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04