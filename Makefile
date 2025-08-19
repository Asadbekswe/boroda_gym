mig:
	python3 manage.py makemigrations
	python3 manage.py migrate


.PHONY: celery beat flower

celery:
	celery -A root worker -l INFO

beat:
	celery -A root beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

flower:
	celery -A root flower --port=5001

celery-all:
	celery -A root worker -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
