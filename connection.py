from pymongo import MongoClient
import settings

client = MongoClient(settings.mongodb_url, settings.port)
db = client['HelpDesk']