from typing import Dict, List, Type, Any, Optional

from notion_client import Client

from .page import NotionPage
from .properties import property_factory, NotionProperty, UnsupportedProperty


class NotionDatabase:
    def __init__(self, notion_client: Client, database_id: str):
        self.client = notion_client
        self.database_id = database_id
        self.properties: Dict[str, NotionProperty] = self.get_schema()

    def get_schema(self) -> Dict[str, NotionProperty]:
        """Load the database schema and create property mappings"""
        db_info = self.client.databases.retrieve(database_id=self.database_id)
        props = {}
        for prop_name, prop_info in db_info.get("properties", {}).items():
            try:
                props[prop_name] = property_factory(prop_info["type"], prop_name)
            except Exception as e:
                print(f"Warning: Failed to create property {prop_name}: {e}")
                props[prop_name] = UnsupportedProperty(prop_name)
        return props

    def query(self, **filters) -> List[NotionPage]:
        """Query the database with filters"""
        if filters:
            results = self.client.databases.query(database_id=self.database_id, filter=self._build_filter(filters))
        else:
            results = self.client.databases.query(database_id=self.database_id)
        return [NotionPage(self, page) for page in results["results"]]

    def _build_filter(self, filters: dict) -> dict:
        """Convert Python-style filters to Notion API filter format"""
        # This is a basic implementation - you might want to expand it
        notion_filters = []
        for prop, value in filters.items():
            notion_filters.append({"property": prop, "equals": value})

        return {"and": notion_filters} if len(notion_filters) > 1 else notion_filters[0] if notion_filters else {}

    def get_page(self, page_id: str) -> NotionPage:
        """Get a page and return it as a NotionPage object"""
        page = self.client.pages.retrieve(page_id=page_id)
        return NotionPage(self, page)

    def update_page(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Update a page's properties"""
        notion_properties = {
            prop_name: self.properties[prop_name].__class__.to_notion(value)
            for prop_name, value in properties.items()
            if prop_name in self.properties
        }
        return self.client.pages.update(
            page_id=page_id,
            properties=notion_properties
        )

    def create_page(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new page in the database"""
        notion_properties = {
            prop_name: self.properties[prop_name].__class__.to_notion(value)
            for prop_name, value in properties.items()
            if prop_name in self.properties
        }
        return self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=notion_properties
        )