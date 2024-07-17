from pydantic import BaseModel
from typing import Optional


class Blog(BaseModel):
    title: str
    body: str
    published : bool | None = False
    

class UpdateBlog(BaseModel):
    title: str | None = ""
    body: str | None = ""
    published : bool | None = False