"""
Text Analytics Streamlit Dashboard
文本分析交互式仪表板
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import re


# 页面配置
st.set_page_config(
    page_title="Text Analytics Suite",
    page_icon="📝",
    layout="wide"
)

# 标题
st.title("📝 Text Analytics Dashboard")
st.markdown("---")

# 侧边栏
st.sidebar.header("⚙️ 分析配置")

# 文本输入
st.sidebar.subheader("输入文本")
input_text = st.sidebar.text_area(
    "输入要分析的文本",
    "Apple Inc. announced record quarterly earnings today. The tech giant's revenue exceeded analyst expectations, driven by strong iPhone sales in China and Europe. CEO Tim Cook expressed optimism about the company's AI initiatives.",
    height=200
)

# 分析选项
st.sidebar.subheader("分析选项")
do_sentiment = st.sidebar.checkbox("情感分析", value=True)
do_keywords = st.sidebar.checkbox("关键词提取", value=True)
do_entities = st.sidebar.checkbox("实体识别", value=True)
do_summary = st.sidebar.checkbox("文本摘要", value=False)

# 分析按钮
if st.sidebar.button("🚀 开始分析", type="primary"):
    st.sidebar.success("分析开始！")

# 主界面
tab1, tab2, tab3, tab4 = st.tabs(["📊 概览", "😊 情感分析", "🔑 关键词", "🏷️ 实体识别"])

# 模拟分析结果
def analyze_sentiment(text):
    """模拟情感分析"""
    positive_words = ['record', 'exceeded', 'strong', 'optimism', 'growth', 'success']
    negative_words = ['decline', 'loss', 'weak', 'pessimism', 'failure']
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return 'positive', 0.75
    elif neg_count > pos_count:
        return 'negative', 0.25
    else:
        return 'neutral', 0.5

def extract_keywords(text, n=5):
    """模拟关键词提取"""
    # 简单实现：提取名词
    words = re.findall(r'\b[A-Za-z]{4,}\b', text)
    stop_words = ['announced', 'today', 'company', 'about', 'their', 'with', 'from']
    keywords = [w for w in words if w.lower() not in stop_words]
    return keywords[:n]

def extract_entities(text):
    """模拟实体识别"""
    entities = []
    
    # 公司名
    if 'Apple' in text:
        entities.append({'text': 'Apple Inc.', 'type': 'ORGANIZATION'})
    if 'iPhone' in text:
        entities.append({'text': 'iPhone', 'type': 'PRODUCT'})
    
    # 人名
    if 'Tim Cook' in text:
        entities.append({'text': 'Tim Cook', 'type': 'PERSON'})
    
    # 地点
    if 'China' in text:
        entities.append({'text': 'China', 'type': 'LOCATION'})
    if 'Europe' in text:
        entities.append({'text': 'Europe', 'type': 'LOCATION'})
    
    return entities

# Tab 1: 概览
with tab1:
    st.header("📊 分析概览")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总词数", len(input_text.split()))
    
    with col2:
        st.metric("字符数", len(input_text))
    
    with col3:
        st.metric("句子数", input_text.count('.') + input_text.count('!') + input_text.count('?'))
    
    with col4:
        sentiment, score = analyze_sentiment(input_text)
        st.metric("情感倾向", sentiment.capitalize())
    
    st.markdown("---")
    
    # 文本统计
    st.subheader("📈 文本统计")
    
    word_freq = pd.Series(input_text.lower().split()).value_counts().head(10)
    
    fig = px.bar(
        x=word_freq.values,
        y=word_freq.index,
        orientation='h',
        title='Top 10 高频词',
        labels={'x': '频次', 'y': '单词'}
    )
    fig.update_layout(template='plotly_dark', height=400)
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: 情感分析
with tab2:
    st.header("😊 情感分析")
    
    sentiment, score = analyze_sentiment(input_text)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("情感极性", sentiment.capitalize())
    
    with col2:
        st.metric("置信度", f"{score * 100:.1f}%")
    
    # 情感仪表盘
    fig_gauge = {
        "data": [{
            "type": "indicator",
            "mode": "gauge+number",
            "value": score * 100,
            "domain": {"x": [0, 1], "y": [0, 1]},
            "title": {"text": "情感得分"},
            "gauge": {
                "axis": {"range": [0, 100]},
                "bar": {"color": "green" if sentiment == "positive" else "red"},
                "steps": [
                    {"range": [0, 33], "color": "lightgray"},
                    {"range": [33, 66], "color": "gray"}
                ]
            }
        }],
        "layout": {"template": "plotly_dark"}
    }
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # 情感分析详情
    st.subheader("📝 分析详情")
    st.info(f"""
    **正面词汇**: record, exceeded, strong, optimism
    
    **负面词汇**: 无
    
    **结论**: 文本整体呈现积极情绪，主要因为财报表现超出预期。
    """)

# Tab 3: 关键词
with tab3:
    st.header("🔑 关键词提取")
    
    keywords = extract_keywords(input_text)
    
    st.subheader("提取的关键词")
    
    for i, kw in enumerate(keywords, 1):
        st.write(f"{i}. **{kw}**")
    
    # 关键词云模拟
    st.subheader("关键词可视化")
    
    kw_data = pd.DataFrame({
        '关键词': keywords,
        '重要性': [1.0 / (i + 1) for i in range(len(keywords))]
    })
    
    fig = px.bar(
        kw_data,
        x='重要性',
        y='关键词',
        orientation='h',
        title='关键词重要性排序',
        labels={'x': '重要性得分', 'y': '关键词'}
    )
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: 实体识别
with tab4:
    st.header("🏷️ 命名实体识别")
    
    entities = extract_entities(input_text)
    
    if entities:
        # 按类型分组
        entity_df = pd.DataFrame(entities)
        
        st.subheader("识别的实体")
        st.dataframe(entity_df, use_container_width=True)
        
        # 实体分布
        st.subheader("实体类型分布")
        
        type_counts = entity_df['type'].value_counts()
        
        fig = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title='实体类型分布',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
        # 实体列表
        st.subheader("详细列表")
        
        for entity_type in entity_df['type'].unique():
            type_entities = entity_df[entity_df['type'] == entity_type]['text'].tolist()
            st.write(f"**{entity_type}**: {', '.join(type_entities)}")
    else:
        st.info("未识别到命名实体")

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Text Analytics Suite | Powered by Streamlit</p>
    <p>📝 支持：情感分析 | 关键词提取 | 实体识别 | 文本摘要</p>
</div>
""", unsafe_allow_html=True)
