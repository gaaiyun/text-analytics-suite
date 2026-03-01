#!/usr/bin/env python3
"""
Text Analytics - Named Entity Recognition
"""

from typing import List, Dict
import re


class NERExtractor:
    """Named Entity Recognition"""
    
    def __init__(self):
        # Simple patterns for demo
        self.patterns = {
            'PERSON': r'[\u4e00-\u9fa5]{2,4}(?:先生|女士|教授|博士)?',
            'ORG': r'[\u4e00-\u9fa5]{2,}(?:公司|集团|大学|学院|研究所)',
            'LOC': r'[\u4e00-\u9fa5]{2,}(?:市|省|区|县|镇|村)',
            'DATE': r'\d{4}年\d{1,2}月\d{1,2}日'
        }
    
    def extract(self, text: str) -> List[Dict]:
        """Extract named entities"""
        entities = []
        
        for entity_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                entities.append({
                    'text': match.group(),
                    'type': entity_type,
                    'start': match.start(),
                    'end': match.end()
                })
        
        return sorted(entities, key=lambda x: x['start'])


def main():
    text = "马云在2019年9月10日宣布卸任阿里巴巴集团董事局主席，张勇接任。"
    
    ner = NERExtractor()
    entities = ner.extract(text)
    
    print("Entities:")
    for entity in entities:
        print(f"  {entity['text']} ({entity['type']})")


if __name__ == '__main__':
    main()
