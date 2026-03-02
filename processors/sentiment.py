#!/usr/bin/env python3
"""Sentiment analysis processor"""
from typing import Dict, List
from textblob import TextBlob
import pandas as pd


class SentimentAnalyzer:
    """Analyze sentiment of text"""
    
    def __init__(self, method: str = 'textblob'):
        self.method = method
    
    def analyze(self, text: str) -> Dict[str, float]:
        """Analyze sentiment"""
        if self.method == 'textblob':
            return self._textblob_sentiment(text)
        return {'polarity': 0.0, 'subjectivity': 0.0}
    
    def _textblob_sentiment(self, text: str) -> Dict[str, float]:
        """TextBlob sentiment"""
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity,
            'label': self._get_label(blob.sentiment.polarity)
        }
    
    def _get_label(self, polarity: float) -> str:
        """Get sentiment label"""
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        return 'neutral'
    
    def batch_analyze(self, texts: List[str]) -> pd.DataFrame:
        """Analyze multiple texts"""
        results = [self.analyze(text) for text in texts]
        return pd.DataFrame(results)
