dumpfile := "../dev_data.json"

.PHONY: dump load

dump:
	python manage.py dumpdata --indent 2 --exclude admin --exclude auth --exclude contenttypes --exclude sessions > ${dumpfile}

load:
	python manage.py loaddata ${dumpfile}
