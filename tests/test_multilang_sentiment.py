"""multilang_sentiment.py 测试 —— 中英文情感 + auto routing。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from processors.multilang_sentiment import (
    SentimentScore,
    _is_chinese,
    _label_from_polarity,
    _lexicon_chinese,
    aggregate,
    analyze,
    analyze_batch,
)


# --- _is_chinese ----------------------------------------------------

def test_is_chinese_pure_cn():
    assert _is_chinese("这是中文文本") is True


def test_is_chinese_pure_en():
    assert _is_chinese("This is pure English") is False


def test_is_chinese_mixed_heavy_cn():
    assert _is_chinese("产品很好 great") is True


def test_is_chinese_empty():
    assert _is_chinese("") is False


def test_is_chinese_threshold_low_catches_short_cn():
    # 一个中文字符在 10 字符中 = 10%
    assert _is_chinese("a b c 好 d e", threshold=0.05) is True


# --- _label_from_polarity -------------------------------------------

def test_label_positive():
    assert _label_from_polarity(0.5) == "positive"


def test_label_negative():
    assert _label_from_polarity(-0.5) == "negative"


def test_label_neutral():
    assert _label_from_polarity(0.01) == "neutral"
    assert _label_from_polarity(0.0) == "neutral"


def test_label_custom_threshold():
    assert _label_from_polarity(0.05, threshold=0.10) == "neutral"
    assert _label_from_polarity(0.15, threshold=0.10) == "positive"


# --- _lexicon_chinese -----------------------------------------------

def test_lexicon_positive_chinese():
    s = _lexicon_chinese("这个产品真好，性价比高，很满意")
    assert s.polarity > 0
    assert s.label == "positive"
    assert s.backend == "lexicon"


def test_lexicon_negative_chinese():
    s = _lexicon_chinese("产品太差，质量糟糕，完全失望，要退货")
    assert s.polarity < 0
    assert s.label == "negative"


def test_lexicon_no_hits_neutral():
    s = _lexicon_chinese("今天去公园")
    assert s.label == "neutral"
    assert s.confidence == 0.0


def test_lexicon_confidence_scales_with_hits():
    low = _lexicon_chinese("还可以")
    high = _lexicon_chinese("好，棒，赞，优秀，完美，喜欢，满意")
    assert high.confidence > low.confidence


# --- analyze 端到端 -------------------------------------------------

def test_analyze_empty_returns_neutral():
    s = analyze("")
    assert s.label == "neutral"
    assert s.polarity == 0.0


def test_analyze_whitespace_returns_neutral():
    s = analyze("   \n\t   ")
    assert s.label == "neutral"


def test_analyze_auto_routes_chinese():
    s = analyze("产品很好，非常满意")
    # SnowNLP 或 lexicon 都可以；只要不是 textblob/vader
    assert s.backend in ("snownlp", "lexicon")


def test_analyze_auto_routes_english():
    s = analyze("This product is fantastic and amazing!")
    # 英文：vader 或 textblob
    assert s.backend in ("vader", "textblob")


def test_analyze_force_textblob():
    s = analyze("This is good", backend="textblob")
    assert s.backend == "textblob"


def test_analyze_force_lexicon():
    s = analyze("产品很好", backend="lexicon")
    assert s.backend == "lexicon"
    assert s.polarity > 0


def test_analyze_vader_missing_raises(monkeypatch):
    """显式 backend=vader 但没装时应 raise。"""
    import builtins
    real = builtins.__import__

    def fake(name, *a, **kw):
        if name == "vaderSentiment.vaderSentiment":
            raise ImportError("simulated")
        return real(name, *a, **kw)

    monkeypatch.setattr(builtins, "__import__", fake)
    with pytest.raises(RuntimeError, match="vaderSentiment"):
        analyze("text", backend="vader")


def test_analyze_snownlp_missing_raises(monkeypatch):
    import builtins
    real = builtins.__import__

    def fake(name, *a, **kw):
        if name == "snownlp":
            raise ImportError("simulated")
        return real(name, *a, **kw)

    monkeypatch.setattr(builtins, "__import__", fake)
    with pytest.raises(RuntimeError, match="snownlp"):
        analyze("text", backend="snownlp")


def test_analyze_to_dict_serializable():
    import json
    s = analyze("Great product!")
    json.dumps(s.to_dict())


# --- analyze_batch --------------------------------------------------

def test_batch_returns_list():
    results = analyze_batch(["good", "bad", "ok"])
    assert len(results) == 3
    assert all(isinstance(r, SentimentScore) for r in results)


def test_batch_mixed_languages():
    results = analyze_batch(["This is great", "产品很好", "neutral text"])
    assert len(results) == 3


# --- aggregate ------------------------------------------------------

def test_aggregate_empty():
    a = aggregate([])
    assert a["n"] == 0
    assert a["signal"] == "neutral"


def test_aggregate_mean_polarity():
    scores = [
        SentimentScore(polarity=0.8, label="positive", backend="vader"),
        SentimentScore(polarity=0.6, label="positive", backend="vader"),
        SentimentScore(polarity=-0.2, label="negative", backend="vader"),
    ]
    a = aggregate(scores)
    assert a["n"] == 3
    assert abs(a["mean_polarity"] - 0.4) < 1e-9
    assert a["signal"] == "positive"


def test_aggregate_label_distribution():
    scores = [
        SentimentScore(polarity=0.5, label="positive", backend="x"),
        SentimentScore(polarity=0.5, label="positive", backend="x"),
        SentimentScore(polarity=-0.5, label="negative", backend="x"),
    ]
    a = aggregate(scores)
    assert a["label_dist"]["positive"] == 2
    assert a["label_dist"]["negative"] == 1


def test_aggregate_balanced_neutral_signal():
    scores = [
        SentimentScore(polarity=0.5, label="positive", backend="x"),
        SentimentScore(polarity=-0.5, label="negative", backend="x"),
    ]
    a = aggregate(scores)
    assert abs(a["mean_polarity"]) < 1e-9
    assert a["signal"] == "neutral"
