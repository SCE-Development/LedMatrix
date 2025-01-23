from pydantic import BaseModel
#user schema
from typing import Optional
class Users(BaseModel):
    __tablename__='users'
    username:str
    api_key:str
    easy_solved:int=0
    medium_solved:int=0
    hard_solved:int=0


    @property
    def total_solved(self) -> int:
        return self.easy_solved + self.medium_solved + self.hard_solved
    
    @property
    def points(self) -> int:
        return self.easy_solved + 3 * self.medium_solved + 5 * self.hard_solved

    class Config:
        orm_mode=True

