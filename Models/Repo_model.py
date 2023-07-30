from pydantic import BaseModel
from typing import Optional

class Repo(BaseModel):
    username: Optional[str]
    name: Optional[str]
    description: Optional[str]
    language: Optional[str]
    forks_count: int
    stargazers_count: int
    subscribers_count: int
    contributor_count: int

