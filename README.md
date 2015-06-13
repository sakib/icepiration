Icepiration Global Calendar tech asset repository. Flask App in development.

To get set up on the project:

1. Set up virtualenv
    - run "virtualenv -p python3 venv"
    - to activate run "source venv/bin/activate"
    - to deactivate run "deactivate"
2. Use pip to install dependencies (in the virtualenv)
    - run "pip install -r pip.req"
    - run "pip install -i https://testpypi.python.org/pypi Flask-Auth"
    - run "pip install https://launchpad.net/oursql/py3k/py3k-0.9.4/+download/oursql-0.9.4.zip":
3. Run "python run.py"

Database stuff:

Ubuntu: sudo apt-get install mysql-server libmysqlclient-dev
Run the following commands:
- "sudo mysql"
- "create database ice;"
- "create user 'ice'@'localhost' identified by 'password';"
- "grant all privileges on ice.* to 'ice'@'localhost';"
- "flush privileges"
Quit out of mysql. Then run:
- "python db_create.py"
