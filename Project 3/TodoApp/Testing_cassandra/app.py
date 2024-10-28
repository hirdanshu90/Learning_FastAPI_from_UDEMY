from fastapi import FastAPI, HTTPException
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid
from pydantic import BaseModel, EmailStr




# Define the Pydantic model for the user data
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

# Define the Pydantic model for updating user data
class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    age: int


# Initialize FastAPI app
app = FastAPI()

# Configure Cassandra connection
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra node IPs
session = cluster.connect('my_keyspace')  # Replace 'my_keyspace' with your keyspace

# Prepare CRUD queries (prepared statements)
create_user_stmt = session.prepare("""
    INSERT INTO users (user_id, name, email, age) VALUES (?, ?, ?, ?)
""")
get_user_stmt = session.prepare("""
    SELECT * FROM users WHERE user_id = ?
""")
update_user_stmt = session.prepare("""
    UPDATE users SET name = ?, email = ?, age = ? WHERE user_id = ?
""")
delete_user_stmt = session.prepare("""
    DELETE FROM users WHERE user_id = ?
""")

# Basic User Model (UUID and User Data)
class User:
    
    def __init__(self, user_id, name, email, age):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.age = age

@app.post("/users/")
async def create_user(user: UserCreate):
    user_id = uuid.uuid4()  # Generate a unique UUID for the new user
    session.execute(create_user_stmt, [user_id, user.name, user.email, user.age])
    return {"user_id": str(user_id), "name": user.name, "email": user.email, "age": user.age}


# Read a user (GET /users/{user_id})
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        result = session.execute(get_user_stmt, [uuid.UUID(user_id)]).one()
        if result:
            return {"user_id": str(result.user_id), "name": result.name, "email": result.email, "age": result.age}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Update a user (PUT /users/{user_id})
@app.put("/users/{user_id}")
async def update_user(user_id: str, user: UserUpdate):
    session.execute(update_user_stmt, [user.name, user.email, user.age, uuid.UUID(user_id)])
    return {"user_id": user_id, "name": user.name, "email": user.email, "age": user.age}


# Delete a user (DELETE /users/{user_id})
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        session.execute(delete_user_stmt, [uuid.UUID(user_id)])
        return {"detail": f"User {user_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run the FastAPI app with uvicorn
# Run the following command to start the server:
# uvicorn app:app --reload
