"""
AI Legal Advisor - Professional Frontend Application
Enterprise-grade IT Legal Risk Assessment Platform
"""

import streamlit as st
from input_filter import InputFilter
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="AI Legal Advisor - IT Legal Risk Assessment",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# プロフェッショナルなカスタムCSS
st.markdown("""
    <style>
    /* グローバルフォント */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* ヘッダー */
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* リスクレベルカード */
    .risk-card {
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid #e5e7eb;
    }
    
    .risk-high {
        background-color: #fef2f2;
        border-left: 4px solid #dc2626;
    }
    
    .risk-medium {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
    }
    
    .risk-low {
        background-color: #f0fdf4;
        border-left: 4px solid #10b981;
    }
    
    .risk-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6b7280;
        margin-bottom: 0.5rem;
    }
    
    .risk-value {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }
    
    /* セクション */
    .section-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #374151;
        margin-top: 2rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* 法律バッジ */
    .law-badge {
        display: inline-block;
        background-color: #f3f4f6;
        color: #374151;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem 0.25rem 0.25rem 0;
    }
    
    /* 推奨事項リスト */
    .recommendation-item {
        padding: 0.75rem 0;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .recommendation-item:last-child {
        border-bottom: none;
    }
    
    /* 情報ボックス */
    .info-box {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* ボタンスタイル調整 */
    .stButton button {
        border-radius: 6px;
        font-weight: 500;
        border: 1px solid #e5e7eb;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        border-color: #d1d5db;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* サイドバー */
    [data-testid="stSidebar"] {
        background-color: #f9fafb;
    }
    
    /* フッター */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.875rem;
        padding: 3rem 0 2rem 0;
        border-top: 1px solid #e5e7eb;
        margin-top: 4rem;
    }
    
    /* 入力エリア */
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #d1d5db;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown('<div class="main-header">AI Legal Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Enterprise IT Legal Risk Assessment Platform</div>', unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.markdown("### Coverage")
    
    st.markdown("""
    **Supported Areas**
    
    • Personal Information Protection  
    • Consumer Protection  
    • Web Accessibility  
    • Financial Regulations  
    • Contract Law
    """)
    
    st.divider()
    
    st.markdown("### Out of Scope")
    
    st.markdown("""
    • OSS Licensing  
    • AI Ethics  
    • Technical Implementation
    """)
    
    st.divider()
    
    st.markdown("### Settings")
    show_debug = st.checkbox("Show debug information", value=False)
    
    st.divider()
    
    st.markdown("""
    <div style='font-size: 0.75rem; color: #6b7280; line-height: 1.6;'>
    <strong>Disclaimer</strong><br>
    This assessment is for reference only. 
    Please consult with legal counsel for final decisions.
    </div>
    """, unsafe_allow_html=True)

# 関数定義
def generate_mock_result(input_text: str):
    """モック結果生成"""
    if "位置情報" in input_text or "個人情報" in input_text:
        return {
            "risk_level": "Medium",
            "risk_level_ja": "中",
            "laws": ["Personal Information Protection Act", "Telecommunications Business Act"],
            "reason": "位置情報は個人を特定できる情報であり、収集時には目的を限定した開示が義務付けられています。また、広告配信事業者への提供は、提供先が適切な措置を講じているかの確認が必要です。",
            "recommendations": [
                "プライバシーポリシーに位置情報の収集目的を明記してください。",
                "提供先との間で個人情報の第三者提供に関する契約（NDA）を締結してください。",
                "ユーザーに対してオプトアウト機会を提供してください。"
            ],
            "inference_time": 15.2,
        }
    elif "解約" in input_text or "ダークパターン" in input_text:
        return {
            "risk_level": "High",
            "risk_level_ja": "高",
            "laws": ["Specified Commercial Transactions Act", "Consumer Contract Act"],
            "reason": "解約を不当に困難にするUI（ダークパターン）が見られ、不当な顧客囲い込みとみなされるリスクがあります。",
            "recommendations": [
                "解約ボタンは視認性の高い位置に配置してください。",
                "解約を選択したユーザーには適切なサポートを提供してください。",
                "警告メッセージは1回までに制限することを推奨します。"
            ],
            "inference_time": 12.8,
        }
    elif "アクセシビリティ" in input_text or "代替テキスト" in input_text or "画像" in input_text:
        return {
            "risk_level": "Medium",
            "risk_level_ja": "中",
            "laws": ["Act on Elimination of Discrimination against Persons with Disabilities"],
            "reason": "スクリーンリーダーで画像の内容が読み上げられないことは、情報伝達における不備として認定される可能性があります。",
            "recommendations": [
                "画像ボタンにはテキストバッジを設置してください。",
                "代替テキスト（alt属性）を必ず記載してください。",
                "JIS X 8341-3に準拠した実装を行ってください。"
            ],
            "inference_time": 14.5,
        }
    else:
        return {
            "risk_level": "Medium",
            "risk_level_ja": "中",
            "laws": ["Under Review"],
            "reason": "入力内容に基づいて法的リスクを分析しています。より詳細な情報があれば、精度が向上します。",
            "recommendations": [
                "具体的な仕様を追加してください。",
                "ユーザーデータの取り扱いについて明記してください。",
                "法務担当者に確認することを推奨します。"
            ],
            "inference_time": 10.0,
        }

def display_result(result: dict, show_debug: bool = False):
    """結果表示"""
    risk_level = result["risk_level"]
    
    # リスクレベルカード
    if risk_level == "High":
        risk_class = "risk-high"
        risk_color = "#dc2626"
    elif risk_level == "Medium":
        risk_class = "risk-medium"
        risk_color = "#f59e0b"
    else:
        risk_class = "risk-low"
        risk_color = "#10b981"
    
    st.markdown(f"""
    <div class="risk-card {risk_class}">
        <div class="risk-label">Risk Level</div>
        <div class="risk-value" style="color: {risk_color};">{risk_level}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 該当法律
    st.markdown('<div class="section-title">Applicable Laws</div>', unsafe_allow_html=True)
    
    laws_html = "".join([f'<span class="law-badge">{law}</span>' for law in result["laws"]])
    st.markdown(f'<div>{laws_html}</div>', unsafe_allow_html=True)
    
    # リスクの理由
    st.markdown('<div class="section-title">Risk Analysis</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color: #374151; line-height: 1.6;">{result["reason"]}</div>', unsafe_allow_html=True)
    
    # 推奨事項
    st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)
    
    for i, rec in enumerate(result["recommendations"], 1):
        st.markdown(f"""
        <div class="recommendation-item">
            <strong style="color: #6b7280;">{i}.</strong> {rec}
        </div>
        """, unsafe_allow_html=True)
    
    # エクスポート
    st.markdown('<div class="section-title">Export Results</div>', unsafe_allow_html=True)
    
    copy_text = f"""AI Legal Advisor - Risk Assessment Report

Risk Level: {risk_level}

Applicable Laws:
{chr(10).join(['• ' + law for law in result["laws"]])}

Risk Analysis:
{result["reason"]}

Recommendations:
{chr(10).join([f'{i}. {rec}' for i, rec in enumerate(result["recommendations"], 1)])}

---
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Disclaimer: This assessment is for reference only. Please consult with legal counsel.
"""
    
    st.text_area(
        "Copy report:",
        value=copy_text,
        height=200,
        label_visibility="collapsed"
    )
    
    if show_debug:
        st.markdown('<div class="section-title">Debug Information</div>', unsafe_allow_html=True)
        st.json({
            "risk_level": result["risk_level"],
            "laws": result["laws"],
            "inference_time": f"{result['inference_time']:.2f}s",
        })

# session_state初期化
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''

# メインコンテンツ
st.markdown('<div class="section-title">Specification Input</div>', unsafe_allow_html=True)

# サンプルケース
col1, col2, col3 = st.columns(3)

sample_texts = {
    "sample1": "ユーザーの位置情報を収集して、第三者の広告配信事業者に提供します。",
    "sample2": "解約ボタンを画面の一番下に小さく配置し、その上に『本当に解約しますか？多くの特典を失います』という警告を3回表示します。",
    "sample3": "重要な操作ボタンを画像のみで表示し、代替テキストを設定していません。"
}

with col1:
    if st.button("Example: Location Data", use_container_width=True):
        st.session_state['user_input'] = sample_texts["sample1"]
        st.rerun()

with col2:
    if st.button("Example: Dark Pattern", use_container_width=True):
        st.session_state['user_input'] = sample_texts["sample2"]
        st.rerun()

with col3:
    if st.button("Example: Accessibility", use_container_width=True):
        st.session_state['user_input'] = sample_texts["sample3"]
        st.rerun()

st.write("")  # スペース

# 入力フォーム
user_input = st.text_area(
    "Enter specification to assess:",
    value=st.session_state['user_input'],
    height=120,
    placeholder="Example: We collect user location data and share it with third-party advertising providers.",
    label_visibility="collapsed"
)

if user_input != st.session_state['user_input']:
    st.session_state['user_input'] = user_input

# アクションボタン
col_clear, col_space, col_check = st.columns([1, 2, 2])

with col_clear:
    if st.button("Clear", use_container_width=True):
        st.session_state['user_input'] = ''
        st.rerun()

with col_check:
    check_button = st.button("Assess Risk", type="primary", use_container_width=True)

# 判定処理
if check_button:
    if not user_input or user_input.strip() == "":
        st.warning("Please enter a specification to assess.")
    else:
        # 入力フィルタリング
        filter_obj = InputFilter()
        is_in_scope, message, category = filter_obj.check_scope(user_input)
        
        if not is_in_scope:
            st.error(f"Out of Scope: {category}")
            st.markdown(f"""
            <div class="warning-box">
                <strong>Notice</strong><br>
                {message}
            </div>
            """, unsafe_allow_html=True)
            
            if show_debug:
                st.json({
                    "is_in_scope": is_in_scope,
                    "category": category,
                    "message": message
                })
        else:
            # モック結果表示
            with st.spinner("Analyzing legal risks..."):
                import time
                time.sleep(0.5)  # UX向上のための短い遅延
                
                mock_result = generate_mock_result(user_input)
                
                st.markdown("---")
                st.markdown('<div class="section-title">Assessment Results</div>', unsafe_allow_html=True)
                
                display_result(mock_result, show_debug)

# フッター
st.markdown("""
<div class="footer">
    <strong>AI Legal Advisor Platform</strong><br>
    Powered by Fine-tuned Elyza-7B | Version 1.0.0<br>
    © 2026 AI Legal Advisor. All rights reserved.
</div>
""", unsafe_allow_html=True)
