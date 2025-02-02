from abc import ABC
from enum import Enum
from typing import Any, Dict, List, Optional, TypedDict, Type 
from notion_client import Client

class NotionProperty(ABC):
    notion_name: str
    
    def __init__(self, name: str):
        self.name = name

    def to_notion(self, value: Any) -> Dict[str, Any]:
        """Convert a Python value to a Notion property value"""
        raise NotImplementedError
        
    def from_notion(self, value: Dict[str, Any]) -> Any:
        """Convert a Notion property value to a Python value"""
        raise NotImplementedError

    @classmethod
    def get_property_mapping(cls) -> Dict[str, Type['NotionProperty']]:
        """Returns a mapping of notion property types to their corresponding classes"""
        return {subclass.notion_name: subclass for subclass in cls.__subclasses__()}

class TextProperty(NotionProperty):
    notion_name = "rich_text"
    
    def to_notion(self, value: str) -> Dict[str, Any]:
        return {"rich_text": [{"text": {"content": value}}]}
    
    def from_notion(self, value: Dict[str, Any]) -> str:
        return value.get("rich_text", [{}])[0].get("text", {}).get("content", "")

class CheckboxProperty(NotionProperty):
    notion_name = "checkbox"
    
    def to_notion(self, value: bool) -> Dict[str, Any]:
        return {"checkbox": value}
    
    def from_notion(self, value: Dict[str, Any]) -> bool:
        return value.get("checkbox", False)

class PeopleProperty(NotionProperty):
    notion_name = "people"
    
    def to_notion(self, value: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"people": value}
    
    def from_notion(self, value: Dict[str, Any]) -> List[Dict[str, Any]]:
        return value.get("people", [])

class StatusProperty(NotionProperty):
    notion_name = "status"
    
    def to_notion(self, value: str) -> Dict[str, Any]:
        return {"status": {"name": value}}
    
    def from_notion(self, value: Dict[str, Any]) -> str:
        return value.get("status", {}).get("name", "")

class SelectProperty(NotionProperty):
    notion_name = "select"
    
    def to_notion(self, value: str) -> Dict[str, Any]:
        return {"select": {"name": value}}
    
    def from_notion(self, value: Dict[str, Any]) -> str:
        return value.get("select", {}).get("name", "")

class MultiSelectProperty(NotionProperty):
    notion_name = "multi_select"
    
    def to_notion(self, value: List[str]) -> Dict[str, Any]:
        return {"multi_select": [{"name": v} for v in value]}
    
    def from_notion(self, value: Dict[str, Any]) -> List[str]:
        return [item["name"] for item in value.get("multi_select", [])]

class TitleProperty(NotionProperty):
    notion_name = "title"
    
    def to_notion(self, value: str) -> Dict[str, Any]:
        return {"title": [{"text": {"content": value}}]}
    
    def from_notion(self, value: Dict[str, Any]) -> str:
        return value.get("title", [{}])[0].get("text", {}).get("content", "")

def property_factory(type: str, name: str) -> NotionProperty:
    """Creates the appropriate property type based on Notion schema"""
    property_mapping = NotionProperty.get_property_mapping()
    return property_mapping[type](name) 