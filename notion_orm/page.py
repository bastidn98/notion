from typing import Any, Dict

class NotionPage:
    def __init__(self, database, page_data: Dict):
        self.database = database
        self.id = page_data['id']
        self._raw_data = page_data
        self._properties = {}
        self._load_properties()
    
    def _load_properties(self):
        """Load properties from raw page data"""
        for name, prop in self._raw_data['properties'].items():
            if name in self.database.properties:
                self._properties[name] = self.database.properties[name].from_notion(prop)
    
    def __getattr__(self, name: str) -> Any:
        """Allow accessing properties as attributes"""
        if name in self._properties:
            return self._properties[name]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")
    
    def update(self, **properties):
        """Update page properties"""
        notion_properties = {
            name: self.database.properties[name].to_notion(value)
            for name, value in properties.items()
        }
        
        self._raw_data = self.database.client.pages.update(
            page_id=self.id,
            properties=notion_properties
        )
        self._load_properties() 