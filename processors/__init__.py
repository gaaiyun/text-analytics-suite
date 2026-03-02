"""Text processing modules"""
from .sentiment import SentimentAnalyzer
from .keywords import KeywordExtractor
from .summarizer import TextSummarizer
from .classifier import TextClassifier
from .entity_extractor import EntityExtractor

__all__ = ['SentimentAnalyzer', 'KeywordExtractor', 'TextSummarizer', 'TextClassifier', 'EntityExtractor']
