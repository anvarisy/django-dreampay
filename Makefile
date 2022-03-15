.PHONY: run
run:
	@python dreampay/manage.py runserver

.PHONY: admin
admin:
	@python dreampay/manage.py createsuperuser

.PHONY: migrations
migrations:
	@python dreampay/manage.py makemigrations

.PHONY: migrate
migrate:
	@python dreampay/manage.py migrate