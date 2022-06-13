dumpfile := "../dev_data.json"

.PHONY: dump load lint

dump:
	python manage.py dumpdata --indent 2 --exclude admin --exclude auth --exclude contenttypes --exclude sessions > ${dumpfile}

load:
	python manage.py loaddata ${dumpfile}

lint:
	pylint ./**/*.py --ignore-paths="venv,.*migrations" -d R0903

lint_wo_doc:
	pylint ./**/*.py --ignore-paths="venv,.*migrations" -d R0903 -d C0114 -d C0115 -d C0116