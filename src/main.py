import psycopg, yaml, random
from fastapi import FastAPI

# config file related
print("reading and setting up config file...")
def update_config(config:dict[str, str | int]) -> dict[str, str | int]:
    with open("config.yaml", "w+") as config_file:
        yaml.dump(config, config_file)
    return config

try:
    with open("config.yaml") as config_file:
        config = yaml.safe_load(config_file)
except FileNotFoundError:
    print("Config file does not exist, creating it...")
    config = update_config({"db_exists": False})

# setup server
print("setting up server methods...")
server = FastAPI()

@server.get("/")
async def root():
    return {"message": "welcome to the server. use /create/{id} and /read/{id}"}

@server.get("/create/{username}")
async def create(username:str):
    await create_no_pooling(username)
    return {"message": f"the listing for {username} has been created."}

@server.get("/read/{username}")
async def read(username:str):
    user_id = await read_no_pooling(username)
    return {"message": f"the ID for username {username} is {user_id}"}

# setup db
print("setting up database...")
with psycopg.connect("dbname=postgres user=postgres password=sush1342") as db:
    with db.cursor() as db_cursor:
        if not config["db_exists"]:
            db_cursor.execute("CREATE TABLE users_task_one (id integer, username text)")
            config["db_exists"] = True
            config = update_config(config)

async def create_no_pooling(username:str) -> None:
    async with await psycopg.AsyncConnection.connect(f"dbname=postgres user=postgres password=sush1342") as async_conn:
        async with async_conn.cursor() as async_cursor:
            await async_cursor.execute("INSERT INTO users_task_one (id, username) VALUES (%s, %s)", (random.randint(0, 255), username))
            await async_conn.commit()

# BROKEN - DO NOT USE
async def read_no_pooling(username:str) -> str:
    async with await psycopg.AsyncConnection.connect(f"dbname=postgres user=postgres password=sush1342") as async_conn:
        async with async_conn.cursor() as async_cursor:
            print("one")
            await async_cursor.execute("SELECT id, username FROM users_task_one WHERE username=%s", (username))
            print("two")
            await async_cursor.fetchone()
            print("three")
            async for record in async_cursor:
                print(record, type(record))
            print("four")
    return 'true'
