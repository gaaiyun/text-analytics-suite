# Text Analytics Suite

📝 **综合文本分析工具集 - NLP 数据处理神器**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests: 17/17](https://img.shields.io/badge/tests-17%2F17%20passed-brightgreen.svg)](tests/)

---

## 📋 项目概述

Text Analytics Suite 是一个**综合文本分析工具集**，提供情感分析、关键词提取、实体识别、文本摘要等 NLP 功能。基于 Streamlit 的交互式仪表板让文本分析变得简单直观。

**核心特点**：
- 📝 **5 大核心功能** - 情感/关键词/实体/摘要/分类
- 📊 **Streamlit UI** - 交互式分析界面
- 🔄 **批量处理** - 文档流水线分析
- 💾 **多格式导出** - CSV/JSON/Markdown 报告
- ✅ **完整测试** - 17/17 单元测试通过

---

## 🚀 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 运行 Dashboard

```bash
streamlit run dashboard.py
```

访问 http://localhost:8501

### 命令行使用

```bash
# 情感分析
python scripts/sentiment.py --text "Great product!"

# 关键词提取
python scripts/keywords.py --file article.txt

# 实体识别
python scripts/ner.py --text "Apple Inc. is in California"
```

---

## 📁 项目结构

```
Text-Analytics-Suite/
├── processors/          # 分析处理器
│   ├── sentiment.py    # 情感分析
│   ├── keywords.py     # 关键词提取
│   ├── entity_extractor.py  # 实体识别
│   ├── summarizer.py   # 文本摘要
│   └── classifier.py   # 文本分类
├── scripts/            # 命令行脚本
├── pipeline/           # 批量处理
│   └── document_analyzer.py
├── dashboard.py        # Streamlit 界面
├── tests/              # 单元测试
│   └── test_analytics.py  # 17/17 通过 ✅
├── utils/              # 工具函数
├── requirements.txt    # 依赖
└── README.md           # 本文档
```

---

## 🎯 核心功能

### 1. 情感分析 😊

分析文本情感倾向（正面/负面/中性）

```python
from processors.sentiment import SentimentAnalyzer

analyzer = SentimentAnalyzer()
result = analyzer.analyze("Excellent product, highly recommend!")
# {'sentiment': 'positive', 'score': 0.92}
```

### 2. 关键词提取 🔑

提取文本核心关键词

```python
from processors.keywords import KeywordExtractor

extractor = KeywordExtractor()
keywords = extractor.extract(text, top_k=5)
```

### 3. 实体识别 🏷️

识别命名实体（人名/地名/机构名）

```python
from processors.entity_extractor import EntityExtractor

extractor = EntityExtractor()
entities = extractor.extract("Apple CEO Tim Cook visited Beijing")
# [{'text': 'Apple', 'type': 'ORG'}, {'text': 'Tim Cook', 'type': 'PERSON'}]
```

### 4. 文本摘要 📝

自动生成文本摘要

```python
from processors.summarizer import Summarizer

summarizer = Summarizer()
summary = summarizer.summarize(long_text, max_length=100)
```

### 5. 文本分类 📂

自动文本分类

```python
from processors.classifier import TextClassifier

classifier = TextClassifier()
category = classifier.classify(text)
```

---

## 📊 Streamlit Dashboard 功能

### 分析概览
- 词数统计
- 字符数统计
- 句子数统计
- 情感倾向

### 情感分析
- 情感极性（正面/负面/中性）
- 置信度得分
- 情感仪表盘可视化

### 关键词提取
- Top 关键词列表
- 词频统计图
- 关键词重要性排序

### 实体识别
- 实体列表（按类型分组）
- 实体类型分布饼图
- 详细实体信息

---

## 🔄 文档批量分析

批量处理文本文档：

```python
from pipeline.document_analyzer import DocumentAnalyzer

analyzer = DocumentAnalyzer(
    input_dir='./documents',
    output_dir='./output'
)

# 分析所有文档
df = analyzer.analyze_all('.txt')

# 自动生成：
# - CSV 结果
# - JSON 结果
# - 汇总报告（Markdown）
```

### 输出内容
- 词数统计
- 可读性分数
- 高频词分析
- 汇总报告

---

## 🧪 测试

运行所有测试：

```bash
pytest tests/ -v
```

**测试结果**: 17/17 通过 ✅

```
test_sentiment_analysis.py::test_positive_sentiment PASSED
test_sentiment_analysis.py::test_negative_sentiment PASSED
test_keyword_extraction.py::test_extract_words PASSED
test_entity_recognition.py::test_extract_organization PASSED
...
```

---

## 💡 使用场景

| 场景 | 功能 | 输出 |
|------|------|------|
| 产品评论分析 | 情感分析 | 正面/负面比例 |
| 新闻监控 | 实体识别 + 关键词 | 关键事件提取 |
| 文档整理 | 批量分析 | 分类 + 摘要 |
| 市场调研 | 文本分类 | 主题分布 |
| 社交媒体监控 | 情感 + 实体 | 品牌声誉分析 |

---

## 📚 相关资源

- [NLTK 文档](https://www.nltk.org/)
- [spaCy 文档](https://spacy.io/)
- [TextBlob 文档](https://textblob.readthedocs.io/)
- [Streamlit 文档](https://docs.streamlit.io/)

---

## 📝 更新日志

### 2026-03-02
- ✅ 添加 Streamlit Dashboard
- ✅ 添加文档批量分析流水线
- ✅ 完善情感分析和实体识别可视化
- ✅ 添加 17 个单元测试（100% 通过）
- ✅ 完善 README 文档

---

## 👤 作者

**GitHub**: [gaaiyun](https://github.com/gaaiyun)

**技能展示**：
- 🔧 Python 全栈开发
- 📊 NLP/文本分析
- 💼 商业分析
- 🚀 快速原型开发

---

## 📄 许可证

MIT License

---

_最后更新：2026-03-02_
