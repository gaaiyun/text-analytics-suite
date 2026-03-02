#!/usr/bin/env python3
"""Named entity extraction processor"""
from typing import List, Dict
import re


class EntityExtractor:
    """Extract named entities from text"""
    
    def __init__(self):
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'url': r'https?://[^\s]+',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'money': r'\$\d+(?:,\d{3})*(?:\.\d{2})?'
        }
    
    def extract(self, text: str) -> Dict[str, List[str]]:
        """Extract all entities"""
        entities = {}
        
        for entity_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                entities[entity_type] = list(set(matches))
        
        return entities
    
    def extract_type(self, text: str, entity_type: str) -> List[str]:
        """Extract specific entity type"""
        pattern = self.patterns.get(entity_type)
        if not pattern:
            return []
        
        matches = re.findall(pattern, text)
        return list(set(matches))
    
    def add_pattern(self, entity_type: str, pattern: str):
        """Add custom entity pattern"""
        self.patterns[entity_type] = pattern
