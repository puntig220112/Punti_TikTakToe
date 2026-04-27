from pydantic import BaseModel

class UserCreate(BaseModel):
    user_name: str
    password: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    user_name: str

    model_config = {
        "from_attributes": True
    }
