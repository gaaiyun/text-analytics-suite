---
name: text-analytics-suite
description: Comprehensive text analytics toolkit for sentiment analysis, keyword extraction, text classification, NER, and summarization. Perfect for showcasing NLP and text processing skills.
---

# Text Analytics Suite Skill

## 1. 什么时候用我？

当用户说：
- "分析这段文本的情感"
- "提取关键词"
- "文本分类"
- "识别实体"
- "生成摘要"
- 任何文本分析需求

## 2. 我能做什么？

### 情感分析
- **多语言支持** - 中文、英文情感分析
- **细粒度分析** - 正面、负面、中性
- **情感强度** - 0-1 分数
- **方面级情感** - 针对特定主题

### 关键词提取
- **TF-IDF** - 统计方法
- **TextRank** - 图算法
- **RAKE** - 快速自动提取
- **YAKE** - 无监督方法

### 文本分类
- **主题分类** - 新闻、评论、文档
- **意图识别** - 用户意图分析
- **垃圾检测** - 垃圾邮件、评论
- **自定义分类** - 训练自己的模型

### 命名实体识别 (NER)
- **人名** - 识别人物
- **地名** - 识别地点
- **机构名** - 识别组织
- **时间** - 识别日期时间
- **自定义实体** - 领域特定实体

### 文本摘要
- **抽取式摘要** - 提取关键句子
- **生成式摘要** - AI 生成摘要
- **多文档摘要** - 合并多个文档
- **可控长度** - 指定摘要长度

## 3. 使用示例

### 情感分析
```python
from text_analytics import SentimentAnalyzer

analyzer = SentimentAnalyzer(language='zh')
result = analyzer.analyze("这个产品非常好用！")
print(result)
# {'sentiment': 'positive', 'score': 0.95, 'confidence': 0.92}
```

### 关键词提取
```python
from text_analytics import KeywordExtractor

extractor = KeywordExtractor(method='textrank')
keywords = extractor.extract(text, top_k=10)
print(keywords)
# ['机器学习', '深度学习', '神经网络', ...]
```

### 文本分类
```python
from text_analytics import TextClassifier

classifier = TextClassifier(model='news')
category = classifier.classify("今天股市大涨...")
print(category)
# {'category': '财经', 'confidence': 0.88}
```

### 命名实体识别
```python
from text_analytics import NERExtractor

ner = NERExtractor()
entities = ner.extract("马云在杭州创立了阿里巴巴")
print(entities)
# [{'text': '马云', 'type': 'PERSON'}, 
#  {'text': '杭州', 'type': 'LOC'},
#  {'text': '阿里巴巴', 'type': 'ORG'}]
```

### 文本摘要
```python
from text_analytics import TextSummarizer

summarizer = TextSummarizer(method='extractive')
summary = summarizer.summarize(long_text, max_length=100)
print(summary)
```

## 4. 命令行使用

```bash
# 情感分析
python scripts/sentiment.py --text "这个产品很好" --language zh

# 关键词提取
python scripts/keywords.py --file article.txt --top 10

# 文本分类
python scripts/classify.py --text "今天天气很好" --model topic

# 实体识别
python scripts/ner.py --file document.txt --output entities.json

# 文本摘要
python scripts/summarize.py --file article.txt --length 200
```

## 5. 展示价值

### NLP 能力 ⭐⭐⭐⭐⭐
- 多种 NLP 任务
- 中英文支持
- 高准确率

### 文本处理能力 ⭐⭐⭐⭐⭐
- 数据清洗
- 特征提取
- 结果可视化

### 工程能力 ⭐⭐⭐⭐⭐
- 模块化设计
- 易于扩展
- 完整文档

## 6. 依赖项

```txt
transformers>=4.30.0
torch>=2.0.0
jieba>=0.42.0
textblob>=0.17.0
spacy>=3.5.0
nltk>=3.8.0
scikit-learn>=1.3.0
```

## 7. 安装

```bash
pip install transformers torch jieba textblob spacy nltk scikit-learn
python -m spacy download zh_core_web_sm
python -m spacy download en_core_web_sm
```

---

_基于 Transformers, spaCy, NLTK 开发_
_OpenClaw Skill 封装版本_
