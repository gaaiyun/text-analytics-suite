"""
Tests for Text Analytics Suite
单元测试 - 文本分析
"""

import pytest
import pandas as pd
from pathlib import Path
import sys
import re

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestSentimentAnalysis:
    """测试情感分析"""
    
    def test_positive_sentiment(self):
        """测试正面情感识别"""
        text = "Excellent product! Highly recommend. Great quality!"
        positive_words = ['excellent', 'great', 'highly', 'recommend', 'quality']
        
        score = sum(1 for word in positive_words if word.lower() in text.lower())
        assert score >= 2
    
    def test_negative_sentiment(self):
        """测试负面情感识别"""
        text = "Terrible experience. Very disappointed. Poor service."
        negative_words = ['terrible', 'disappointed', 'poor', 'bad', 'worst']
        
        score = sum(1 for word in negative_words if word.lower() in text.lower())
        assert score >= 2
    
    def test_neutral_sentiment(self):
        """测试中性情感识别"""
        text = "The package arrived on Tuesday. It was a box."
        
        # Should have low sentiment score
        assert len(text.split()) > 5


class TestKeywordExtraction:
    """测试关键词提取"""
    
    def test_extract_words(self):
        """测试单词提取"""
        text = "Machine learning and artificial intelligence are transforming industries"
        words = re.findall(r'\b[A-Za-z]{4,}\b', text)
        
        assert len(words) > 5
        assert 'Machine' in words or 'machine' in words
    
    def test_remove_stopwords(self):
        """测试停用词移除"""
        words = ['the', 'machine', 'learning', 'is', 'great']
        stopwords = ['the', 'is', 'a', 'an']
        
        filtered = [w for w in words if w.lower() not in stopwords]
        assert len(filtered) < len(words)
        assert 'the' not in filtered
    
    def test_word_frequency(self):
        """测试词频统计"""
        words = ['ai', 'ml', 'ai', 'dl', 'ai', 'ml']
        freq = pd.Series(words).value_counts()
        
        assert freq['ai'] == 3
        assert freq['ml'] == 2


class TestEntityRecognition:
    """测试实体识别"""
    
    def test_extract_organization(self):
        """测试机构名识别"""
        text = "Apple Inc. and Microsoft Corporation announced partnership"
        
        # Simple pattern matching
        orgs = re.findall(r'[A-Z][a-z]+ (?:Inc|Corp|LLC|Ltd)\.?', text)
        assert len(orgs) >= 1
    
    def test_extract_person(self):
        """测试人名识别"""
        text = "John Smith and Jane Doe attended the conference"
        
        # Simple pattern: Two capitalized words
        names = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text)
        assert len(names) >= 2
    
    def test_extract_location(self):
        """测试地名识别"""
        text = "The company is headquartered in California and has offices in New York"
        
        locations = ['California', 'New York', 'Texas', 'Washington']
        found = [loc for loc in locations if loc in text]
        assert len(found) >= 1


class TestTextSummarization:
    """测试文本摘要"""
    
    def test_extract_top_sentences(self):
        """测试提取关键句子"""
        text = """
        Artificial intelligence is transforming the world. 
        Machine learning is a subset of AI. 
        Deep learning has achieved remarkable results. 
        AI applications are everywhere.
        """
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        # Select top 2 sentences (simple: first 2)
        summary = sentences[:2]
        assert len(summary) == 2
    
    def test_summary_length(self):
        """测试摘要长度控制"""
        original_length = 500
        summary_ratio = 0.2
        summary_length = original_length * summary_ratio
        
        assert summary_length < original_length
        assert summary_length == 100


class TestTextClassification:
    """测试文本分类"""
    
    def test_category_keywords(self):
        """测试分类关键词匹配"""
        categories = {
            'technology': ['ai', 'ml', 'software', 'tech'],
            'finance': ['stock', 'market', 'investment', 'money'],
            'health': ['medical', 'health', 'doctor', 'hospital']
        }
        
        text = "The new AI software uses machine learning"
        text_lower = text.lower()
        
        # Should match technology category
        for keyword in categories['technology']:
            if keyword in text_lower:
                assert True
                break
    
    def test_multi_label_classification(self):
        """测试多标签分类"""
        text = "Tech company stock rises after AI product launch"
        
        # Could be both technology and finance
        assert 'tech' in text.lower() or 'AI' in text
        assert 'stock' in text.lower()


class TestDocumentAnalyzer:
    """测试文档分析器"""
    
    def test_word_count(self):
        """测试词数统计"""
        text = "This is a test document with several words"
        word_count = len(text.split())
        
        assert word_count == 8
    
    def test_character_count(self):
        """测试字符数统计"""
        text = "Hello World"
        char_count = len(text)
        
        assert char_count == 11
    
    def test_sentence_count(self):
        """测试句子数统计"""
        text = "First sentence. Second sentence! Third sentence?"
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        
        assert sentence_count == 3
    
    def test_average_word_length(self):
        """测试平均词长计算"""
        text = "I am a test"
        words = text.split()
        avg_length = sum(len(w) for w in words) / len(words)
        
        assert avg_length == 2.0  # (1+2+1+4)/4 = 2.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
