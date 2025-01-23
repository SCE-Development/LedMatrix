from sqllite_helper import update_user,display_all_user
import time
import schedule
from schemas.userSchemas import Users
from main import get_db_file
import aiohttp
import ssl
import certifi
from fastapi import HTTPException
from secureApi import API_KEY
import asyncio


# constants file 

ssl_context = ssl.create_default_context(cafile=certifi.where())
leetcode_client_url="http://localhost:8000"

def run_updated_db(function):
   asyncio.run(function())


async def update_hourly():

    db_file=get_db_file()
    db_entries=display_all_user(db_file) 

    print("Starting to update")
   

    for user_entry in db_entries:
        username=user_entry[0]
        api_key=API_KEY[0] #this is the api key for the first item in the api key, need to find a way to fix this

        user=Users(username=username,api_key=api_key) 
        url=f'{leetcode_client_url}/{username}' 

        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
                async with session.get(f'{url}') as response: 
                   
                    if(response.status == 200 ):
                
                        data=await response.json()                        
                        user.easy_solved=data['EASY']
                        user.medium_solved=data['MEDIUM']
                        user.hard_solved=data['HARD']
                    else:
                        print(f"Error {response.status_code}")
                        raise HTTPException(status_code=response.status)

        except Exception as e:
            raise HTTPException(status_code=500, detail={e})

                
        update_user(db_file,user.username,user.total_solved,user.points,user.easy_solved,user.medium_solved,user.hard_solved)

        print(f"Updated user{user.username}")


last=None
#schedule.every(10).seconds.do(run_updated_db,update_hourly) # for testing
schedule.every(1).hour.do(run_updated_db,update_hourly)

print()
while True:
    schedule.run_pending()
    next_run=schedule.next_run()
    if next_run!=last:
        print(f"Updating at: {next_run}") # prints out when the next time the update is going to be availiable 

    last=next_run
    time.sleep(1)