1. pip install poetry (or safer, follow the instructions: https://python-poetry.org/docs/#installation)
2. Install dependencies cd into the directory where the pyproject.toml is located then poetry install
    poetry lock
    poetry install
3. In a terminal: uvicorn main:app --reload
Open http://localhost:8001/


to make jinja work:
.venv/lib/python3.10/site-packages/starlette/templating.py
replace:
    @jinja2.contextfunction
    @jinja2.pass_context

adding new module/library:
1. Go to pyproject.toml , add the respective module or dependencies
2. To install dependencies, cd into the directory where the pyproject.toml is located then:
   poetry lock
   poetry install