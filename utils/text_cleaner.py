#!/usr/bin/env python3
"""Text cleaning utilities"""
import re
from typing import List


class TextCleaner:
    """Clean and normalize text"""
    
    @staticmethod
    def clean(text: str, lowercase: bool = True, remove_punctuation: bool = False) -> str:
        """Clean text"""
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        if remove_punctuation:
            text = re.sub(r'[^\w\s]', '', text)
        
        return text.strip()
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs"""
        return re.sub(r'https?://\S+', '', text)
    
    @staticmethod
    def remove_emails(text: str) -> str:
        """Remove emails"""
        return re.sub(r'\S+@\S+', '', text)
    
    @staticmethod
    def remove_numbers(text: str) -> str:
        """Remove numbers"""
        return re.sub(r'\d+', '', text)
    
    @staticmethod
    def remove_special_chars(text: str) -> str:
        """Remove special characters"""
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace"""
        return ' '.join(text.split())
