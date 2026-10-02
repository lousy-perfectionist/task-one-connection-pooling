# Task 1 - Connection Pooling Demo
## Installation
Run the following commands to install and setup the database. Replace [password] with the password to your PostgreSQL postgre database.
```bash
python -m pip install -r requirements.txt
python src/main.py [password]
```
## Usage
Start the FastAPI server using,
```bash
python -m fastapi dev
```
Then, in another terminal, run the load testing with locust using,
```bash
# use the following to test without connection pooling
python -m locust -f src/load_testing.py --host http://127.0.0.1:8000 --tags no_pooling
# use the following to test with connection pooling
python -m locust -f src/load_testing.py --host http://127.0.0.1:8000 --tags with_pooling
```

## Test Case
For each case, 
- total of concurrent requests = 100
- ramp-up (users started/second) = 10
- total time = 1 min
- query used = `INSERT INTO users_task_one (id, username) VALUES (a random id, username)`
- pool size = 4+; dynamically assigned by `psycorpg`

## Resuts

| case | total requests over 1 min | average requests/sec | faliure rate | avg response time |
| --- | --- | --- | --- | --- |
| without pooling | 3217 | 51.3rps | 0% | 1800ms |
| with pooling | 18163 | 298.6rps | 0% | 310ms |

## Explanation
Clearly, connection pooling shows massive performance benefits. This is most likely due to the fact that one database connection handles multiple users; which saves the massive overhead of creating new connections each time.