# 🚀 FastAPI + MongoDB Sample Project

This is a small CRUD project built using **FastAPI** and **MongoDB** (via `motor`) with a configurable setup using environment variables.

---

## 📦 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — Modern async web framework
- [Motor](https://motor.readthedocs.io/) — Async MongoDB driver
- [Pydantic](https://docs.pydantic.dev/) — Data validation
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Load environment variables

---
## 🧪 Install & Run

### Prerequisites

* python 3.10 or Latest 


### Installation

1. Creating virtual environments
    
    ```sh
    python -m venv /venv
    ```
3. Install Requirement packages
   
    ```sh
    pip install -r requirements.txt
    ```

### Start Server
* Run app
	
	```sh
    fastapi dev .\main.py
    ```
   will see: http://127.0.0.1:8000 local service

### References

  * Fast API: https://fastapi.tiangolo.com
  * MongoDB: https://www.mongodb.com
   
