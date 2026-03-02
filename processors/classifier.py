#!/usr/bin/env python3
"""Text classification processor"""
from typing import List, Dict
from collections import Counter


class TextClassifier:
    """Classify text into categories"""
    
    def __init__(self):
        self.categories = {
            'business': ['business', 'company', 'market', 'finance', 'economy'],
            'technology': ['technology', 'software', 'computer', 'ai', 'data'],
            'sports': ['sports', 'game', 'team', 'player', 'match'],
            'politics': ['politics', 'government', 'election', 'policy', 'law'],
            'entertainment': ['movie', 'music', 'celebrity', 'show', 'entertainment']
        }
    
    def classify(self, text: str) -> Dict[str, float]:
        """Classify text"""
        text_lower = text.lower()
        scores = {}
        
        for category, keywords in self.categories.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[category] = score
        
        total = sum(scores.values())
        if total > 0:
            scores = {k: v/total for k, v in scores.items()}
        
        return scores
    
    def get_top_category(self, text: str) -> str:
        """Get top category"""
        scores = self.classify(text)
        if not scores:
            return 'unknown'
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def add_category(self, name: str, keywords: List[str]):
        """Add custom category"""
        self.categories[name] = keywords
