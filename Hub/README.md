# The Hub

## Overview

The Hub is a backend API built with FastAPI that manages SQLite database relations using SQLModel.

## Requirements

`requirements.txt` contains all required libraries/packages. 

```python
pip install -r requirements.txt
```
Please be in a __Virtual Environment__ before installing dependencies.

## Structure

```
Hub/
│
├── app.py          # Main FastAPI application
├── db.py           # Database setup
├── models.py       # SQLModel schemas
├── relations.py    # Database relationship logic
├── process.py      # Compares value to optimal values
└── requirements.txt
```

## Virtual Environment
It is best practice to use a Python Virtual Environment.
```python
python3 -m venv .venv.     # Create virtual environment
source .venv/bin/activate  # Mac/Linux activation
.\.venv\Scripts\activate   # Windows activation
```

## How to Run
For Development (only runs when outside of Hub folder):
```python
python -m Hub.app
```

For Production:
```python
uvicorn app:app --reload
```

[After running, visit: http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Resources

For more information, please check out the following documents:
- [SQLmodel](https://sqlmodel.tiangolo.com/learn/)
- [FastAPI](https://fastapi.tiangolo.com/learn/)
- [Uvicorn](https://uvicorn.dev)
- [SQLiteBrowser](https://sqlitebrowser.org)
