from locust import HttpUser, task
from requests import JSONDecodeError
from auth import get_bearer_token
import os
from dotenv import load_dotenv

load_dotenv()
HOST_URL = os.getenv("HOST_URL")

class BookingLoadtest(HttpUser):
    headers = {}
    host = HOST_URL
    
    def on_start(self):
        token = get_bearer_token()
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    @task
    def check_tours_endpoint(self):     
        with self.client.get("/v1/tours", headers=self.headers, catch_response=True) as response:
            try:
                if response.status_code != 200:
                    response.failure("Did not get code 200")
            except JSONDecodeError:
                response.failure("Response could not be decoded as JSON")

    @task(1)
    def check_get_tour_details_endpoint(self):     
       with self.client.get("/v1/tours/3eba51fe-6a66-4c9f-b549-e139a841e097", headers=self.headers, catch_response=True) as response:
           try:
               if response.status_code != 200:
                   response.failure("Did not get code 200")
           except JSONDecodeError:
               response.failure("Response could not be decoded as JSON")

    @task(2)
    def check_get_tour_availability_endpoint(self):     
       with self.client.get("/v1/tours/3eba51fe-6a66-4c9f-b549-e139a841e097/options/0335091d-2ee7-44c0-abcb-f54b4ee73862", headers=self.headers, catch_response=True) as response:
           try:
               if response.status_code != 200:
                   response.failure("Did not get code 200")
           except JSONDecodeError:
               response.failure("Response could not be decoded as JSON")