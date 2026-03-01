#!/usr/bin/env python3
"""
Text Analytics - Text Summarization
"""

from typing import List
import jieba
import numpy as np


class TextSummarizer:
    """Text summarization (extractive)"""
    
    def __init__(self, method: str = 'extractive'):
        self.method = method
    
    def summarize(self, text: str, max_length: int = 200) -> str:
        """Generate summary"""
        if self.method == 'extractive':
            return self._extractive_summary(text, max_length)
        else:
            return self._extractive_summary(text, max_length)
    
    def _extractive_summary(self, text: str, max_length: int) -> str:
        """Extractive summarization"""
        # Split into sentences
        sentences = self._split_sentences(text)
        
        if not sentences:
            return ""
        
        # Score sentences
        scores = self._score_sentences(sentences)
        
        # Select top sentences
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        selected_indices = sorted([i for i, _ in ranked[:3]])
        
        summary = ''.join([sentences[i] for i in selected_indices])
        
        if len(summary) > max_length:
            summary = summary[:max_length] + '...'
        
        return summary
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        import re
        sentences = re.split(r'[。！？\n]', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _score_sentences(self, sentences: List[str]) -> List[float]:
        """Score sentences by importance"""
        # Simple scoring: sentence length and position
        scores = []
        for i, sent in enumerate(sentences):
            words = list(jieba.cut(sent))
            length_score = min(len(words) / 20, 1.0)
            position_score = 1.0 / (i + 1)
            scores.append(length_score * 0.7 + position_score * 0.3)
        return scores


def main():
    text = """
    人工智能是计算机科学的一个分支。它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。
    可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。
    """
    
    summarizer = TextSummarizer()
    summary = summarizer.summarize(text, max_length=100)
    
    print("Summary:")
    print(summary)


if __name__ == '__main__':
    main()
