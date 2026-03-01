#!/usr/bin/env python3
"""
Text Analytics - Keyword Extraction
"""

from typing import List, Dict
import jieba.analyse
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class KeywordExtractor:
    """Keyword extraction with multiple methods"""
    
    def __init__(self, method: str = 'textrank', language: str = 'zh'):
        self.method = method
        self.language = language
    
    def extract(self, text: str, top_k: int = 10) -> List[Dict]:
        """Extract keywords"""
        if self.method == 'textrank':
            return self._textrank(text, top_k)
        elif self.method == 'tfidf':
            return self._tfidf(text, top_k)
        else:
            return self._textrank(text, top_k)
    
    def _textrank(self, text: str, top_k: int) -> List[Dict]:
        """TextRank algorithm"""
        if self.language == 'zh':
            keywords = jieba.analyse.textrank(text, topK=top_k, withWeight=True)
            return [{'word': word, 'score': score} for word, score in keywords]
        else:
            # Simple implementation for English
            words = text.lower().split()
            word_freq = {}
            for word in words:
                if len(word) > 3:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [{'word': word, 'score': freq/len(words)} for word, freq in sorted_words[:top_k]]
    
    def _tfidf(self, text: str, top_k: int) -> List[Dict]:
        """TF-IDF method"""
        vectorizer = TfidfVectorizer(max_features=top_k)
        
        if self.language == 'zh':
            words = ' '.join(jieba.cut(text))
            X = vectorizer.fit_transform([words])
        else:
            X = vectorizer.fit_transform([text])
        
        feature_names = vectorizer.get_feature_names_out()
        scores = X.toarray()[0]
        
        keywords = [(feature_names[i], scores[i]) for i in np.argsort(scores)[::-1]]
        return [{'word': word, 'score': score} for word, score in keywords[:top_k]]


def main():
    text_zh = """
    机器学习是人工智能的一个分支。深度学习是机器学习的一个子领域，
    使用神经网络来学习数据的表示。自然语言处理是人工智能的重要应用。
    """
    
    extractor = KeywordExtractor(method='textrank', language='zh')
    keywords = extractor.extract(text_zh, top_k=5)
    
    print("Keywords:")
    for kw in keywords:
        print(f"  {kw['word']}: {kw['score']:.4f}")


if __name__ == '__main__':
    main()
