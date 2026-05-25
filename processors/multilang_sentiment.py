#!/usr/bin/env python3
"""多语言情感分析（v2）。

v1 的 ``SentimentAnalyzer`` 只接 TextBlob，对中文文本输出基本为 0（TextBlob
英文专用）。v2 加自动语言检测 + 路由：

- 中文（CJK 字符占主导）→ 先试 SnowNLP（需要 ``pip install snownlp``），
  装不上时退化到 lexicon-based（内置 ~70 词的极性词典）
- 英文 → 优先 VADER（``pip install vaderSentiment``），它对短文 / 社交媒体
  比 TextBlob 准；缺时退化 TextBlob

API 与 v1 ``SentimentAnalyzer.analyze`` 兼容，所以可以 drop-in 替换。
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional


Backend = Literal["auto", "textblob", "vader", "snownlp", "lexicon"]


@dataclass
class SentimentScore:
    polarity: float          # -1 ~ +1
    label: str               # positive / negative / neutral
    backend: str
    raw_text: str = ""
    confidence: float = 0.0  # 0 ~ 1

    def to_dict(self) -> dict:
        return {
            "polarity": float(self.polarity),
            "label": self.label,
            "backend": self.backend,
            "confidence": float(self.confidence),
        }


# 极简中文极性词典（够 fallback；生产建议接 SnowNLP / HanLP）
_CN_POSITIVE = {
    "好", "棒", "赞", "优秀", "完美", "喜欢", "满意", "推荐", "happy",
    "高兴", "开心", "舒服", "舒适", "美丽", "漂亮", "可爱", "便宜", "划算",
    "超值", "性价比", "实惠", "靠谱", "稳定", "流畅", "快速", "方便",
    "省心", "贴心", "周到", "优惠", "正品", "真好", "不错", "良好", "出色",
}
_CN_NEGATIVE = {
    "差", "烂", "糟糕", "失望", "差评", "不好", "讨厌", "厌恶", "恶心",
    "无语", "心累", "气", "生气", "崩溃", "失败", "翻车", "踩雷", "贵",
    "黑心", "假货", "骗", "诈骗", "慢", "卡", "卡顿", "故障", "破", "坏",
    "丑", "难看", "瑕疵", "劣质", "坑", "套路", "退货", "投诉", "返工",
}


def _is_chinese(text: str, threshold: float = 0.1) -> bool:
    """检测是否中文。CJK 字符占比 > threshold 即视为中文。"""
    if not text:
        return False
    cjk_chars = sum(1 for c in text if "一" <= c <= "鿿")
    return cjk_chars / max(len(text), 1) > threshold


def _label_from_polarity(p: float, threshold: float = 0.05) -> str:
    if p > threshold:
        return "positive"
    if p < -threshold:
        return "negative"
    return "neutral"


def _lexicon_chinese(text: str) -> SentimentScore:
    """中文 lexicon fallback：统计 pos/neg 词数。"""
    pos = sum(1 for w in _CN_POSITIVE if w in text)
    neg = sum(1 for w in _CN_NEGATIVE if w in text)
    total = pos + neg
    if total == 0:
        return SentimentScore(polarity=0.0, label="neutral",
                              backend="lexicon", raw_text=text, confidence=0.0)
    score = (pos - neg) / total
    conf = min(total / 3.0, 1.0)    # 命中越多越自信
    return SentimentScore(
        polarity=score, label=_label_from_polarity(score),
        backend="lexicon", raw_text=text, confidence=conf,
    )


def _try_snownlp(text: str) -> Optional[SentimentScore]:
    try:
        from snownlp import SnowNLP    # type: ignore
    except ImportError:
        return None
    try:
        s = SnowNLP(text)
        p = s.sentiments * 2 - 1     # snownlp 给 [0,1] → 映到 [-1,1]
        return SentimentScore(
            polarity=p, label=_label_from_polarity(p),
            backend="snownlp", raw_text=text, confidence=0.7,
        )
    except Exception:
        return None


def _try_vader(text: str) -> Optional[SentimentScore]:
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer    # type: ignore
    except ImportError:
        return None
    try:
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        # VADER 的 compound ∈ [-1, 1]，自带阈值规则
        compound = scores["compound"]
        return SentimentScore(
            polarity=compound,
            label=_label_from_polarity(compound, threshold=0.05),
            backend="vader", raw_text=text,
            confidence=max(scores["pos"], scores["neg"], scores["neu"]),
        )
    except Exception:
        return None


def _textblob(text: str) -> SentimentScore:
    """v1 兜底 backend（保持向后兼容）。"""
    from textblob import TextBlob
    blob = TextBlob(text)
    p = float(blob.sentiment.polarity)
    return SentimentScore(
        polarity=p, label=_label_from_polarity(p, threshold=0.1),
        backend="textblob", raw_text=text,
        confidence=float(blob.sentiment.subjectivity),
    )


def analyze(text: str, backend: Backend = "auto") -> SentimentScore:
    """分析单段文本情感。

    Parameters
    ----------
    text : 原始文本
    backend : "auto" 自动选；"textblob" / "vader" / "snownlp" / "lexicon"
              强制 backend
    """
    if not text or not text.strip():
        return SentimentScore(polarity=0.0, label="neutral",
                              backend="empty", raw_text=text)

    if backend == "lexicon":
        return _lexicon_chinese(text)
    if backend == "textblob":
        return _textblob(text)
    if backend == "vader":
        result = _try_vader(text)
        if result is None:
            raise RuntimeError("vaderSentiment 未安装：pip install vaderSentiment")
        return result
    if backend == "snownlp":
        result = _try_snownlp(text)
        if result is None:
            raise RuntimeError("snownlp 未安装：pip install snownlp")
        return result

    # auto
    if _is_chinese(text):
        result = _try_snownlp(text)
        if result is not None:
            return result
        return _lexicon_chinese(text)
    # 英文：先试 VADER
    result = _try_vader(text)
    if result is not None:
        return result
    return _textblob(text)


def analyze_batch(texts: List[str], backend: Backend = "auto"
                   ) -> List[SentimentScore]:
    return [analyze(t, backend=backend) for t in texts]


def aggregate(scores: List[SentimentScore]) -> Dict:
    """对一组 score 聚合：均值 polarity / 各 label 占比 / 主导信号。"""
    if not scores:
        return {"n": 0, "mean_polarity": 0.0, "signal": "neutral",
                "label_dist": {}}
    polarities = [s.polarity for s in scores]
    mean_p = sum(polarities) / len(polarities)
    label_dist: Dict[str, int] = {}
    for s in scores:
        label_dist[s.label] = label_dist.get(s.label, 0) + 1
    return {
        "n": len(scores),
        "mean_polarity": float(mean_p),
        "signal": _label_from_polarity(mean_p, threshold=0.05),
        "label_dist": label_dist,
    }
