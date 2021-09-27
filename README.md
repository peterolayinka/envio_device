# Setup Python Virtual Environment

`python3 -m venv venv `

# Activate Environment

`source venv/bin/activate`

# To install dependecies

`. ./startup.sh install` or `pip install -r ./requirements.txt`

# To Run Migration

`python manage.py migrate`

# To start app

`. ./startup.sh run` or `python manage.py runserver`

# To run test

`python manage.py test`

# To run test coverage

`coverage run manage.py test`

# To see coverage report

`coverage report`

# To view API  documetation

Navigate to <basee_url>/swagger/ (e.g http://localhost:8000/swagger/), click and observe the endpoints

## Built with LOVE ❤ by Peter Olayinka with 97% test coverage
