from typing import Dict, List

from notion_client import Client

from .page import NotionPage
from .properties import PropertyType, property_factory


class NotionDatabase:
    def __init__(self, notion_client: Client, database_id: str):
        self.client = notion_client
        self.database_id = database_id
        self.properties: Dict[str, PropertyType] = {}
        self._fetch_schema()

    def _fetch_schema(self):
        """Fetches and caches the database schema from Notion"""
        database = self.client.databases.retrieve(self.database_id)
        self.properties = {name: property_factory(prop_data) for name, prop_data in database["properties"].items()}

    def query(self, **filters) -> List[NotionPage]:
        """Query the database with filters"""
        results = self.client.databases.query(database_id=self.database_id, filter=self._build_filter(filters))
        return [NotionPage(self, page) for page in results["results"]]

    def create_page(self, **properties) -> NotionPage:
        """Create a new page in the database"""
        # Convert Python values to Notion property values
        notion_properties = {name: self.properties[name].to_notion(value) for name, value in properties.items()}

        page = self.client.pages.create(parent={"database_id": self.database_id}, properties=notion_properties)
        return NotionPage(self, page)

    def _build_filter(self, filters: dict) -> dict:
        """Convert Python-style filters to Notion API filter format"""
        # This is a basic implementation - you might want to expand it
        notion_filters = []
        for prop, value in filters.items():
            notion_filters.append({"property": prop, "equals": value})

        return {"and": notion_filters} if len(notion_filters) > 1 else notion_filters[0] if notion_filters else {}
