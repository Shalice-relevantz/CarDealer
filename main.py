from apps import models, dealers, cars
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from apps.database import engine


import logging
import random
import string
import time


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)




models.Base.metadata.create_all(bind=engine)

app = FastAPI()



async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        # you probably want some kind of logging here
        print_exception(e)
        return Response("Internal server error", status_code=500)

app.middleware('http')(catch_exceptions_middleware)


# async def log_requests(request: Request, call_next):
#     idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#     logger.info(f"rid={idem} start request path={request.url.path}")
#     start_time = time.time()
    
#     response = await call_next(request)
    
#     process_time = (time.time() - start_time) * 1000
#     formatted_process_time = '{0:.2f}'.format(process_time)
#     logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
#     return response

# app.middleware('http')(log_requests)



origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(dealers.router, tags=['Dealer'], prefix='/dealer')
app.include_router(cars.router, tags=['Car'], prefix='/car')



# @app.middleware("http")



@app.get("/")
def root():
    return {"message": "Welcome to Car dealer API documentation"}