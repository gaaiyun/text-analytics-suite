#!/usr/bin/env python3
"""Keyword extraction processor"""
from typing import List, Dict
from collections import Counter
import re


class KeywordExtractor:
    """Extract keywords from text"""
    
    def __init__(self, top_n: int = 10):
        self.top_n = top_n
        self.stopwords = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'])
    
    def extract(self, text: str) -> List[Dict[str, any]]:
        """Extract keywords"""
        words = self._tokenize(text)
        words = [w for w in words if w.lower() not in self.stopwords]
        
        counter = Counter(words)
        keywords = []
        
        for word, count in counter.most_common(self.top_n):
            keywords.append({
                'keyword': word,
                'count': count,
                'score': count / len(words) if words else 0
            })
        
        return keywords
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text"""
        text = text.lower()
        words = re.findall(r'\b[a-z]+\b', text)
        return [w for w in words if len(w) > 2]
    
    def extract_phrases(self, text: str, n: int = 2) -> List[str]:
        """Extract n-gram phrases"""
        words = self._tokenize(text)
        phrases = []
        
        for i in range(len(words) - n + 1):
            phrase = ' '.join(words[i:i+n])
            phrases.append(phrase)
        
        counter = Counter(phrases)
        return [phrase for phrase, _ in counter.most_common(self.top_n)]
