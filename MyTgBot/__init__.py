from pyrogram import Client
from pymongo import MongoClient, errors as Mongoerrors
import os
import time

start = time.time()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("TOKEN")


MONGO = "mongodb+srv://kora3244:jNtUZleBWM71f1pC@haremdb.qxtdvdh.mongodb.net/?retryWrites=true&w=majority"
mongo = MongoClient(MONGO)
mongodb = mongo.BOT

try:
   mongodb.server_info()
except Mongoerrors.ConnectionFailure:
     print("Connection failure, INVALID MONGO DB URL!")
     sys.exit()

bot = Client("MyTgBot", 
       api_id=api_id, 
       api_hash=api_hash,
       bot_token=bot_token,
       plugins=dict(root="MyTgBot"), )
