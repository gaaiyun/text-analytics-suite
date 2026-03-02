#!/usr/bin/env python3
"""Text summarization processor"""
from typing import List
import re


class TextSummarizer:
    """Summarize text"""
    
    def __init__(self, ratio: float = 0.3):
        self.ratio = ratio
    
    def summarize(self, text: str, num_sentences: int = None) -> str:
        """Summarize text"""
        sentences = self._split_sentences(text)
        
        if not sentences:
            return ""
        
        if num_sentences is None:
            num_sentences = max(1, int(len(sentences) * self.ratio))
        
        scores = self._score_sentences(sentences)
        top_sentences = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
        
        # Sort by original order
        top_indices = sorted([idx for idx, _ in top_sentences])
        summary = ' '.join([sentences[i] for i in top_indices])
        
        return summary
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _score_sentences(self, sentences: List[str]) -> dict:
        """Score sentences by importance"""
        scores = {}
        
        for i, sentence in enumerate(sentences):
            words = sentence.lower().split()
            score = len(words)  # Simple scoring by length
            scores[i] = score
        
        return scores
    
    def extract_key_sentences(self, text: str, n: int = 3) -> List[str]:
        """Extract key sentences"""
        sentences = self._split_sentences(text)
        scores = self._score_sentences(sentences)
        
        top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
        return [sentences[i] for i, _ in top]
