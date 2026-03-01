#!/usr/bin/env python3
"""
Text Analytics - Sentiment Analysis
"""

from typing import List, Dict, Optional
import jieba
from textblob import TextBlob


class SentimentAnalyzer:
    """Sentiment analysis for Chinese and English"""
    
    def __init__(self, language: str = 'zh'):
        self.language = language
        self.positive_words = set(['好', '棒', '优秀', '喜欢', '推荐'])
        self.negative_words = set(['差', '烂', '糟糕', '失望', '不好'])
    
    def analyze(self, text: str) -> Dict:
        """Analyze sentiment"""
        if self.language == 'zh':
            return self._analyze_chinese(text)
        else:
            return self._analyze_english(text)
    
    def _analyze_chinese(self, text: str) -> Dict:
        """Chinese sentiment analysis"""
        words = jieba.lcut(text)
        
        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        
        if pos_count > neg_count:
            sentiment = 'positive'
            score = min(0.5 + pos_count * 0.1, 1.0)
        elif neg_count > pos_count:
            sentiment = 'negative'
            score = max(0.5 - neg_count * 0.1, 0.0)
        else:
            sentiment = 'neutral'
            score = 0.5
        
        return {
            'sentiment': sentiment,
            'score': score,
            'confidence': abs(score - 0.5) * 2
        }
    
    def _analyze_english(self, text: str) -> Dict:
        """English sentiment analysis"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        score = (polarity + 1) / 2
        
        return {
            'sentiment': sentiment,
            'score': score,
            'confidence': abs(polarity)
        }
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Batch sentiment analysis"""
        return [self.analyze(text) for text in texts]


def main():
    # Chinese example
    analyzer_zh = SentimentAnalyzer(language='zh')
    result = analyzer_zh.analyze("这个产品非常好用，强烈推荐！")
    print(f"Chinese: {result}")
    
    # English example
    analyzer_en = SentimentAnalyzer(language='en')
    result = analyzer_en.analyze("This product is amazing! Highly recommended!")
    print(f"English: {result}")


if __name__ == '__main__':
    main()
