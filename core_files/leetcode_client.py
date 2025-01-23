import ssl
import certifi
import aiohttp
import uvicorn
from fastapi import FastAPI, HTTPException

import constants
# import asyncio
PORT = 8000
HOST = "0.0.0.0"

# Code above tells the website what os are you using and what browser are you using
# from database import add_user

# test_variable='martinceballos123' # myleetcode username
#  MOVE THEST TO CONSTANTS.py
app = FastAPI()
ssl_context = ssl.create_default_context(cafile=certifi.where())
leetCodeUrl = "https://leetcode.com/graphql"

# pass json to parameters

@app.get("/{username}")
async def get_user_stats(username: str):

    # move to contants FIle
    # query = constants.username_query
    query = constants.USERNAME_QUERY
    
    variables = {"userSlug": username}
    # query = constants.headers
    headers = {
        "Content-Type": "application/json",
    }
    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context)
        ) as session:
            async with session.post(
                leetCodeUrl,
                headers=headers,
                json={"query": query, "variables": variables},
            ) as response:
                # print(f"Sending GraphQL request for username: {username}")
                # response=session.post(leetCodeUrl,headers=headers,json={'query':query,'variables':variables})
                # response.raise_for_status() # use session rather than post
                print(f"status code{response.status}")  # for testing

                if response.status == 200:
                    try:
                        data = await response.json()

                        if "errors" in data:
                            raise HTTPException(
                                status_code=404, detail="user cannot be found"
                            )

                        userStats = data["data"]["userProfileUserQuestionProgressV2"][
                            "numAcceptedQuestions"
                        ]
                        return {
                            entry["difficulty"]: entry["count"] for entry in userStats
                        }

                    except Exception as e:
                        print(f"error {e}")

                else:
                    print(f"Status code:{response.status}")
                    raise HTTPException(status_code=400, detail="Invalid Request ")

    except ValueError as e:
        raise HTTPException(status_code=500, details=f"Data error{e}")
    except Exception as e:
        raise HTTPException(status_code=500, details=f"Error occured:{e}")

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8000, log_level="info", use_colors=False)
