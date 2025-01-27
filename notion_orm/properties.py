from enum import Enum
from typing import Any, Dict

class PropertyType(Enum):
    TEXT = "rich_text"
    TITLE = "title"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    CHECKBOX = "checkbox"
    # Add other property types as needed

class BaseProperty:
    def __init__(self, notion_data: Dict):
        self.type = PropertyType(notion_data['type'])
        self.id = notion_data.get('id')
        self.name = notion_data.get('name')
    
    def to_notion(self, value: Any) -> Dict:
        """Convert Python value to Notion API format"""
        raise NotImplementedError
    
    def from_notion(self, notion_value: Dict) -> Any:
        """Convert Notion API value to Python value"""
        raise NotImplementedError

class TextProperty(BaseProperty):
    def to_notion(self, value: str) -> Dict:
        return {
            "rich_text": [{
                "type": "text",
                "text": {"content": value}
            }]
        }
    
    def from_notion(self, notion_value: Dict) -> str:
        rich_text = notion_value.get('rich_text', [])
        return rich_text[0]['text']['content'] if rich_text else ""

def property_factory(notion_data: Dict) -> BaseProperty:
    """Creates the appropriate property type based on Notion schema"""
    prop_type = PropertyType(notion_data['type'])
    # Add mapping for other property types
    type_mapping = {
        PropertyType.TEXT: TextProperty,
        # Add other mappings
    }
    return type_mapping.get(prop_type, BaseProperty)(notion_data) 