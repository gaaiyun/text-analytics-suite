"""advanced_keywords.py 测试 —— TF-IDF + RAKE。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from processors.advanced_keywords import (
    AdvancedKeywordExtractor,
    DEFAULT_STOPWORDS_EN,
    KeywordResult,
    _rake_candidate_phrases,
    _tokenize,
    rake_keywords,
    tfidf_keywords,
)


# --- _tokenize -------------------------------------------------------

def test_tokenize_basic():
    assert _tokenize("Hello World!") == ["hello", "world"]


def test_tokenize_strips_punctuation_and_digits():
    # 'v2' 中 v 与 2 都是 \w → 之间无 \b → "v" 不被匹配，这是 regex 的语义
    assert _tokenize("API v2.0 (2024)") == ["api"]
    # 但用空格隔开就能匹配
    assert _tokenize("API v 2") == ["api", "v"]


def test_tokenize_empty():
    assert _tokenize("") == []


# --- TF-IDF ---------------------------------------------------------

def test_tfidf_returns_keyword_results():
    text = "machine learning algorithms transform data analysis"
    corpus = [text, "data is important", "machine learning is cool",
              "natural language processing"]
    results = tfidf_keywords(text, corpus, top_n=3)
    assert all(isinstance(r, KeywordResult) for r in results)
    assert len(results) <= 3


def test_tfidf_filters_stopwords():
    text = "the the the cat and the dog"
    corpus = [text, "another doc"]
    results = tfidf_keywords(text, corpus, top_n=5)
    # 'the', 'and' 应被过滤
    keywords = {r.keyword for r in results}
    assert "the" not in keywords
    assert "and" not in keywords


def test_tfidf_rare_word_scores_higher():
    """'quantum' 在语料库中只出现 1 次，'data' 在多文档高频 → IDF 让 quantum
    的 IDF 因子 > data 的 IDF 因子（而 TF 部分相同时 quantum score 应该更高）。

    要看 IDF 单独：quantum 出现在 1 doc，data 出现在 4 docs。
    log(5/2)+1 ≈ 1.92 vs log(5/5)+1 = 1.0 → quantum IDF 高于 data。
    """
    text = "quantum analytics data center"
    corpus = [
        text,
        "data center analytics",
        "data science platform",
        "data warehouse infrastructure",
    ]
    results = tfidf_keywords(text, corpus, top_n=10)
    keywords = {r.keyword: r.score for r in results}
    assert "quantum" in keywords
    assert "data" in keywords
    # quantum 在本文 TF=1/4，data 也 TF=1/4，但 quantum 的 IDF 更大
    assert keywords["quantum"] > keywords["data"]


def test_tfidf_empty_corpus_raises():
    with pytest.raises(ValueError, match="corpus"):
        tfidf_keywords("text", [], top_n=5)


def test_tfidf_empty_text_returns_empty():
    results = tfidf_keywords("", ["some corpus"], top_n=5)
    assert results == []


def test_tfidf_respects_min_word_len():
    text = "AI ML NLP machine learning"
    corpus = [text, "machine learning"]
    results = tfidf_keywords(text, corpus, top_n=10, min_word_len=4)
    keywords = {r.keyword for r in results}
    # 'ai' / 'ml' / 'nlp' 长度 < 4 应被过滤
    assert all(len(k) >= 4 for k in keywords)


def test_tfidf_result_to_dict_serializable():
    import json
    text = "test document with keywords"
    corpus = [text, "another doc"]
    results = tfidf_keywords(text, corpus, top_n=2)
    for r in results:
        json.dumps(r.to_dict())


# --- RAKE -----------------------------------------------------------

def test_rake_basic_phrases():
    text = ("Compatibility of systems of linear constraints over the set "
            "of natural numbers")
    results = rake_keywords(text, top_n=5)
    assert all(isinstance(r, KeywordResult) for r in results)
    # 应该提取多词短语而非单词
    assert any(" " in r.keyword for r in results)


def test_rake_extracts_multi_word_phrases():
    text = "Natural language processing helps with text analysis tasks."
    results = rake_keywords(text, top_n=10)
    # 至少有一个多词短语
    multi = [r for r in results if " " in r.keyword]
    assert len(multi) >= 1


def test_rake_stopwords_split_phrases():
    """'the cat and the dog' → 'cat' 和 'dog' 应分开（被 'and' 切）。"""
    text = "the cat and the dog ran fast"
    results = rake_keywords(text, top_n=10)
    keywords = {r.keyword for r in results}
    # 'cat' 和 'dog' 应该是独立 phrase，不是 'cat and dog'
    assert "cat and dog" not in keywords


def test_rake_empty_returns_empty():
    assert rake_keywords("") == []


def test_rake_only_stopwords_empty():
    """全是 stopwords 的输入应返回空。"""
    text = "the a an and or but if in"
    results = rake_keywords(text, top_n=5)
    assert results == []


def test_rake_candidate_phrases_split_correctly():
    phrases = _rake_candidate_phrases("cat and dog. run fast.",
                                       DEFAULT_STOPWORDS_EN)
    # "cat and dog" → "and" 是 stopword → 切成 ["cat"], ["dog"]
    # 然后 "run fast" 是另一句 → ["run", "fast"]
    phrases_str = [" ".join(p) for p in phrases]
    assert "cat" in phrases_str
    assert "dog" in phrases_str
    assert "run fast" in phrases_str


def test_rake_max_phrase_len_filters_long():
    text = " ".join(f"word{i}" for i in range(20))  # 一个 20 词长 phrase
    results = rake_keywords(text, top_n=5, max_phrase_len=3)
    # 没有 stopword 也没有标点 → 整个 20 词是一个候选 phrase，但被
    # max_phrase_len=3 过滤掉 → results 应为空
    assert results == []


def test_rake_score_includes_repeated_phrases():
    """重复出现的短语应该被 RAKE 检测到。"""
    text = ("machine learning is great. machine learning is powerful. "
            "machine learning helps everywhere.")
    results = rake_keywords(text, top_n=10)
    keywords = {r.keyword for r in results}
    # "machine learning" 重复 3 次，应该在结果里（即使不是 top1）
    assert any("machine learning" in k for k in keywords)
    # 其中至少一个 phrase 含 "machine learning"
    ml_entries = [r for r in results if "machine learning" in r.keyword]
    assert len(ml_entries) >= 1
    # raw_count 反映重复
    assert any(r.raw_count >= 2 for r in ml_entries)


# --- AdvancedKeywordExtractor ---------------------------------------

def test_extractor_default_is_rake():
    ext = AdvancedKeywordExtractor()
    assert ext.method == "rake"


def test_extractor_rejects_bad_method():
    with pytest.raises(ValueError, match="method"):
        AdvancedKeywordExtractor(method="bogus")


def test_extractor_rake_no_corpus_needed():
    ext = AdvancedKeywordExtractor(method="rake", top_n=3)
    results = ext.extract("the quick brown fox jumps over lazy dog")
    assert isinstance(results, list)


def test_extractor_tfidf_requires_corpus():
    ext = AdvancedKeywordExtractor(method="tfidf", top_n=3)
    with pytest.raises(ValueError, match="corpus"):
        ext.extract("some text")


def test_extractor_tfidf_with_corpus():
    ext = AdvancedKeywordExtractor(method="tfidf", top_n=3)
    results = ext.extract("machine learning data",
                           corpus=["machine learning data",
                                    "completely different topic about cooking"])
    assert len(results) <= 3
