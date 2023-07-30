from pydantic import BaseModel
from typing import Optional

class User_info(BaseModel):
    login: str
    name: Optional[str]
    email: Optional[str]
    bio: str
    followers: int
    following: int
    public_repos: int
    followers_url: str
    following_url: str
    most_starred_repo: str
    created_at: str
    updated_at: str

class Check_validate(BaseModel):
    type: str
