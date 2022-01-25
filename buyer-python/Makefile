
all: test

test:
	@echo "running tests"
	@pytest

coverage:
	@echo "generating test coverage report"
	@pytest --cov-report=html:cov_html --cov-report=term-missing --cov=buyer buyer/tests

diagram:
	@echo "generating entity-relation diagram to 'doc' folder"
	@python3 buyer/models.py

clean:
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$/)" | xargs rm -rf
	@rm -rf .pytest_cache
	@rm -rf .coverage cov_html

