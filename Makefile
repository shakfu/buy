
all: test

test:
	@echo "running tests"
	@pytest

diagram:
	@echo "generating entity-relation diagram to 'doc' folder"
	@python3 models.py

clean:
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$/)" | xargs rm -rf
	@rm -rf .pytest_cache


