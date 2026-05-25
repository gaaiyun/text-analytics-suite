#!/usr/bin/env python3
"""TF-IDF + RAKE 关键词提取（v2）。

v1 的 ``KeywordExtractor`` 只做词频（top frequency words），对长文章会被
"the / and / company"这种高频但无信息的词主导。v2 加两个学界标准方法：

1. **TF-IDF**（Salton & Buckley 1988）—— 把"在本文档频繁出现但在语料库
   稀有"的词排上来；要求传入参考语料库。

2. **RAKE**（Rose et al. 2010）—— "Rapid Automatic Keyword Extraction"。
   不需要语料库，单文档可用。把文本切分成候选短语（用停用词和标点切），
   按 word degree / word frequency 给短语打分。

参考：
- Rose, Engel, Cramer, Cowley (2010) "Automatic Keyword Extraction from
  Individual Documents", in *Text Mining*, Wiley.
- Salton, Buckley (1988) "Term-weighting approaches in automatic text
  retrieval", *Information Processing & Management*.
"""
from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Set


# 英文常见停用词（够 RAKE / TF-IDF demo）。中文场景应换 jieba.analyse 的内置停用词。
DEFAULT_STOPWORDS_EN = {
    "a", "an", "the", "and", "or", "but", "if", "then", "else", "for",
    "of", "in", "on", "at", "by", "with", "as", "from", "to", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "do",
    "does", "did", "this", "that", "these", "those", "i", "you", "he",
    "she", "it", "we", "they", "them", "their", "his", "her", "its",
    "my", "your", "our", "what", "which", "who", "whom", "whose", "when",
    "where", "why", "how", "all", "any", "both", "each", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own",
    "same", "so", "than", "too", "very", "s", "t", "can", "will", "just",
    "don", "should", "now", "also", "would", "could", "may",
}


@dataclass
class KeywordResult:
    keyword: str
    score: float
    raw_count: int = 0

    def to_dict(self) -> dict:
        return {"keyword": self.keyword,
                "score": float(self.score),
                "raw_count": int(self.raw_count)}


# --- TF-IDF ----------------------------------------------------------------

def _tokenize(text: str) -> List[str]:
    """简单英文分词（保留 a-z 词，小写）。中文用前要先 jieba.cut。"""
    return re.findall(r"\b[a-z]+\b", text.lower())


def tfidf_keywords(
    text: str,
    corpus: Sequence[str],
    top_n: int = 10,
    stopwords: Optional[Set[str]] = None,
    min_word_len: int = 3,
) -> List[KeywordResult]:
    """对单篇 text，基于 corpus 算 TF-IDF。

    Parameters
    ----------
    text : 当前文档
    corpus : 包含当前文档的语料库（list[str]）；越大 IDF 越准
    top_n : 返回前 N 个关键词
    stopwords : 停用词集合（None 用内置英文）
    min_word_len : 最短词长（过滤掉 'i', 'a' 等）
    """
    if not corpus:
        raise ValueError("corpus 不能为空（TF-IDF 需要参考语料库）")
    if stopwords is None:
        stopwords = DEFAULT_STOPWORDS_EN

    def _filter(toks: List[str]) -> List[str]:
        return [w for w in toks
                if w not in stopwords and len(w) >= min_word_len]

    # 词频 (TF)
    doc_tokens = _filter(_tokenize(text))
    if not doc_tokens:
        return []
    tf_counter = Counter(doc_tokens)

    # IDF：在 corpus 中出现该词的文档数
    n_docs = len(corpus)
    doc_freq: defaultdict = defaultdict(int)
    for doc in corpus:
        unique_tokens = set(_filter(_tokenize(doc)))
        for tok in unique_tokens:
            doc_freq[tok] += 1

    # TF-IDF score
    scores: List[KeywordResult] = []
    n_words = len(doc_tokens)
    for word, count in tf_counter.items():
        tf = count / n_words
        df = doc_freq.get(word, 0)
        # smoothed IDF：避免 df=0 时 div-by-zero / log(0)
        idf = math.log((n_docs + 1) / (df + 1)) + 1
        scores.append(KeywordResult(
            keyword=word, score=float(tf * idf), raw_count=count))

    scores.sort(key=lambda r: r.score, reverse=True)
    return scores[:top_n]


# --- RAKE ------------------------------------------------------------------

_SENT_DELIM_PAT = re.compile(
    r"[.!?,;:\n\t\r\(\)\[\]\{\}\"'']|--|\s+-\s+"
)


def _rake_candidate_phrases(text: str, stopwords: Set[str]) -> List[List[str]]:
    """用 stopwords + 标点把句子切成候选短语。每个 phrase 是 list[词]。"""
    # 先用标点切句
    chunks = _SENT_DELIM_PAT.split(text.lower())
    phrases: List[List[str]] = []
    for chunk in chunks:
        tokens = _tokenize(chunk)
        current: List[str] = []
        for tok in tokens:
            if tok in stopwords:
                if current:
                    phrases.append(current)
                    current = []
            else:
                current.append(tok)
        if current:
            phrases.append(current)
    return phrases


def rake_keywords(
    text: str,
    top_n: int = 10,
    stopwords: Optional[Set[str]] = None,
    min_word_len: int = 2,
    max_phrase_len: int = 5,
) -> List[KeywordResult]:
    """Rose 2010 RAKE。无需语料库，单文档可用。

    Algorithm:

    1. 用 stopwords + 标点把 text 切成候选 phrases
    2. 对每个 word w 算：
       - freq(w) = w 在所有 phrases 中出现次数
       - degree(w) = w 所在所有 phrases 的 word counts 之和
    3. word score(w) = degree(w) / freq(w)
    4. phrase score = sum of word scores in phrase
    """
    if stopwords is None:
        stopwords = DEFAULT_STOPWORDS_EN
    phrases = _rake_candidate_phrases(text, stopwords)
    if not phrases:
        return []

    # 过滤太短的词 / 太长的 phrase
    phrases = [
        [w for w in p if len(w) >= min_word_len]
        for p in phrases
    ]
    phrases = [p for p in phrases if 0 < len(p) <= max_phrase_len]
    if not phrases:
        return []

    # 词层面 freq + degree
    word_freq: Counter = Counter()
    word_degree: defaultdict = defaultdict(int)
    for p in phrases:
        # 每个 word 在该 phrase 里：freq += 1，degree += len(phrase)
        # （RAKE 原版定义：degree = sum of co-occurrence counts，等价于 sum
        # of phrase lengths it appears in，因为 phrase 内每个词都共现）
        for w in p:
            word_freq[w] += 1
            word_degree[w] += len(p)

    # word score
    word_score = {
        w: word_degree[w] / freq
        for w, freq in word_freq.items() if freq > 0
    }

    # phrase score = sum word scores
    phrase_score: Counter = Counter()
    phrase_freq: Counter = Counter()
    for p in phrases:
        phrase_str = " ".join(p)
        phrase_score[phrase_str] += sum(word_score.get(w, 0) for w in p)
        phrase_freq[phrase_str] += 1

    # 输出（去重 phrase）
    results = [
        KeywordResult(keyword=phrase, score=score / phrase_freq[phrase],
                       raw_count=phrase_freq[phrase])
        for phrase, score in phrase_score.items()
    ]
    results.sort(key=lambda r: (r.score, r.raw_count), reverse=True)
    return results[:top_n]


# --- 便捷封装 ---------------------------------------------------------------

class AdvancedKeywordExtractor:
    """统一接口：method ∈ {"tfidf", "rake"}。"""

    def __init__(self, method: str = "rake", top_n: int = 10,
                 stopwords: Optional[Set[str]] = None):
        if method not in {"tfidf", "rake"}:
            raise ValueError(f"method 必须 tfidf 或 rake，得到 {method}")
        self.method = method
        self.top_n = top_n
        self.stopwords = stopwords

    def extract(self, text: str,
                corpus: Optional[Sequence[str]] = None) -> List[KeywordResult]:
        if self.method == "tfidf":
            if not corpus:
                raise ValueError("TF-IDF 需要传 corpus（参考语料库 list[str]）")
            return tfidf_keywords(text, corpus, top_n=self.top_n,
                                   stopwords=self.stopwords)
        return rake_keywords(text, top_n=self.top_n,
                              stopwords=self.stopwords)
