from notion_client import Client
from notion_orm import NotionDatabase
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(auth=os.getenv("NOTION_TOKEN"))

db = NotionDatabase(client, os.getenv("NOTION_TICKET_DB_ID"))

pages = db.query()
x=10
