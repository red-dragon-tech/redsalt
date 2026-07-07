.PHONY: validate status

validate:
	python3 scripts/validate.py

status:
	git status --short --branch
