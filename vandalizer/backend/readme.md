sudo systemctl stop redis-server

watchfiles --filter python "celery -A tasks worker -P solo" ./tasks.py