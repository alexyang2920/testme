testme
======

Getting Started
---------------

- Change directory into your newly created project.

    cd testme

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini

- Send Email
	qp --config qp.ini
	https://docs.pylonsproject.org/projects/pyramid-mailer/en/latest/#queue

- Start supervisor
    supervisord -n
