from fastapi import FastAPI,HTTPException,Security,Depends
from schemas.userSchemas import Users
from secureApi import get_api_key
import ssl
import certifi
import aiohttp
from sqllite_helper import create_table,add_user,top_user,display_all_user,check_user_exists,get_first_place,update_all_users_stats
ssl_context = ssl.create_default_context(cafile=certifi.where())
import uvicorn
from fastapi_utils.tasks import repeat_every
import asyncio
from datetime import datetime
import logging  # Add at top
from tabulate import tabulate


#activate env for mac:source macenv/bin/activate

#type this in the terminal to run:uvicorn main:app --reload  (Change main if the file is named differenlty)
#type for leetcode_client:uvicorn leetcode_client:app --host 127.0.0.1 --port 8001 --reload

HOST = "0.0.0.0"
PORT = 8001

app=FastAPI()
leetCodeUrl="http://0.0.0.0:8000"

def get_db_file():
    return 'leetcode.db'


db_file=get_db_file()
create_table(db_file)

@app.post('/register') ## Before /register/{username}
async def register_user(user:Users): # I'm testing the security for the api username:str
    #api_key:str=Security(get_api_key
    # host='http://127.0.0.1:8000'
    #hotspot_host = "http://192.168.1.5:8000" #Temporarily using this host
    
   # user=Users(username=username)
    username=user.username
    api_key=Security(get_api_key(user.api_key))

    url=f"{leetCodeUrl}/{username}"

    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))as session:
            async with session.get(f'{url}') as response:

                print(f'Got response')
                if(response.status == 200):

                    data=await response.json()
                    easy_solved=data['EASY']
                    medium_solved=data['MEDIUM']
                    hard_solved=data["HARD"]
                  
                    #Assigned the user equal to the different fields 
                    user.easy_solved=easy_solved
                    user.medium_solved=medium_solved
                    user.hard_solved=hard_solved
    
                else:
                    raise HTTPException(status_code=response.status,detail="Couldn't get the correct url")
               
    except Exception as e:
        raise HTTPException (f"This is what is occuring in the program{e}")
    db_file=get_db_file() 
                   
    exisiting_user=check_user_exists(db_file, user.username)
    print("Registering user")

    if(not exisiting_user):
        add_user(db_file,user.username,user.total_solved,user.points,user.easy_solved,user.medium_solved,user.hard_solved)
                    #Not already in the db
    return{
        'message':'user registered',
        'userInfo':{
            'username':user.username,
            'total_solved':user.total_solved,
            'points':user.points
        }
    }

@app.get('/leaderboard') # add problems#
def get_users():
    try:
        db_file = get_db_file()
        leaderboard_data = top_user(db_file)
        return leaderboard_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get('/firstPlace')
async def get_top_user():
    db_file=get_db_file()
    
    first_place=get_first_place(db_file)
    print("Access to top user")

    result=[{"username": user[0], "total_solved": user[1],"points":user[2], 'easy_solved':user[3],'medium_solved':user[4],'hard_solved':user[5]} for user in first_place]

    print("Printing out the top user:")
    return result

# Set up logging
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@app.on_event("startup")
@repeat_every(seconds=60)
async def update_stats_periodically() -> None:
    try:
        db_file = get_db_file()
        await update_all_users_stats(db_file)
        logging.info("Updated all users' stats")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Updated all users' stats")
    except Exception as e:
        logging.error(f"Error updating stats: {e}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error updating stats: {e}")
    

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, log_level="info", use_colors=False)