# load testing script - methodology - do 500 writes using the non-pooled case then do 500 more writes using the pooled case, then compare the results.
import time, locust
from sys import argv

print(argv)

# user counter
user_counter = 0
base_user_string = "user"

# server create task
class CreateUserLocust(locust.HttpUser):
    @locust.tag('no_pooling')
    @locust.task
    def create_user(self):
        global user_counter
        self.client.get(f"http://127.0.0.1:8000/create/{base_user_string}_{user_counter}")
        user_counter = user_counter + 1

    @locust.tag('with_pooling')
    @locust.task
    def create_user_pooled(self):
        global user_counter
        self.client.get(f"http://127.0.0.1:8000/create_pooled/{base_user_string}_{user_counter}")
        user_counter = user_counter + 1
