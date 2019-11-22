## Install Pipenv (if not installed)
`run` pip install pipenv

## start virtual environment 
- git clone repo 
- cd flask-sqlachemy-crud
- pipenv shell
- pipenv install

## setup database
`run` cd api  
`run` python  
`run` from app import db  
`run` db.create_all()  
`run` exit()  

## run app 
`run` python run.py 

## POST body
'''
{
    "description": "this is description",
    "name": "product two",
    "price": 3.0,
    "qty": 55
}
'''

## Update is a patch
'''
{
    "description": "this is description",
    "price": 3.0,
    "qty": 55
}
'''