import streamlit as st
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import base64
import time

# 設定読み込み
load_dotenv()

# ==========================================
# 📁 パス設定
# ==========================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, '..', 'assets')

def get_asset_path(filename):
    """assetsフォルダ内のファイルの絶対パスを取得"""
    return os.path.join(ASSETS_DIR, filename)

# ==========================================

# ページ設定
st.set_page_config(
    page_title="Guardian AI - Legal Compliance",
    page_icon="🛡️", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_result' not in st.session_state:
    st.session_state.current_result = None
if 'current_input' not in st.session_state:
    st.session_state.current_input = ""

# ==========================================
# 🎨 CSSデザイン
# ==========================================
st.markdown("""
    <style>
    /* ベースフォント */
    .stApp {
        font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
    }

    /* --- サイドバーのスタイル (修正: 濃度を少し濃く変更) --- */
    section[data-testid="stSidebar"] {
        background-color: #e2e8f0; /* #f8fafcから変更し、より明確なグレーに */
    }

    /* サイドバー見出し */
    .sidebar-label {
        color: #475569;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid #cbd5e1; /* ボーダーも少し濃く */
        padding-bottom: 0.2rem;
    }

    /* --- テキストヘッダーのスタイル調整 --- */
    .custom-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
        padding-top: 10px;
    }
    
    /* 修正: サブヘッダーのフォントサイズを大きく */
    .custom-subheader {
        font-size: 1.6rem; /* 1.4rem -> 1.6rem */
        font-weight: 700;
        color: #334155;
        margin: 0;
        padding-top: 8px; /* アイコンとの位置合わせ調整 */
    }

    /* --- ボタンデザイン --- */
    div.stButton > button {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        color: white;
        border: 1px solid #0f172a;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        background: linear-gradient(145deg, #334155 0%, #475569 100%);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
        transform: translateY(-1px);
        border-color: #475569;
    }
    div.stButton > button:active {
        transform: translateY(0px);
        box-shadow: none;
    }
    
    /* サイドバー内のボタン */
    div[data-testid="stSidebar"] div.stButton > button {
        background: #ffffff;
        color: #334155;
        border: 1px solid #cbd5e1;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        text-align: left;
    }
    div[data-testid="stSidebar"] div.stButton > button:hover {
        background: #f1f5f9;
        border-color: #94a3b8;
        transform: none;
    }

    /* --- リスク判定結果 --- */
    .risk-container {
        padding: 20px 24px; /* 上下のパディングを少し調整 */
        border-radius: 8px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        border: 1px solid #cbd5e1; 
        background-color: #ffffff;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .risk-label {
        font-size: 1.0rem;
        font-weight: 700;
        color: #64748b;
        margin-right: 2rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* 修正: リスク値のフォントサイズを少し小さく */
    .risk-value {
        font-size: 1.8rem; /* 2.2rem -> 1.8rem */
        font-weight: 800;
        font-family: "Georgia", serif;
    }
    
    /* 色定義 */
    .color-High { color: #b91c1c; border-left: 6px solid #b91c1c; }
    .color-Medium { color: #b45309; border-left: 6px solid #b45309; }
    .color-Low { color: #047857; border-left: 6px solid #047857; }
    
    /* 関連法規タグ */
    .law-tag {
        display: inline-block;
        background-color: #f1f5f9;
        color: #334155;
        border: 1px solid #e2e8f0; 
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0 6px 6px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🛠️ ヘルパー関数
# ==========================================

def render_icon_header(text, icon_filename, level="header"):
    """
    アイコンとテキストを表示する関数。
    修正: levelに関わらずカラム比率を統一し、アイコンサイズを揃える。
    """
    full_path = get_asset_path(icon_filename)
    
    if not os.path.exists(full_path):
        if level == "subheader":
            st.subheader(text)
        else:
            st.title(text)
        return

    # 修正: タイトルもサブヘッダーも同じ比率のカラムを使用することで
    # アイコンの表示サイズを統一する ([1.5, 10]程度がバランス良し)
    col_icon, col_text = st.columns([1.5, 10])

    # クラスの切り替え
    text_class = "custom-subheader" if level == "subheader" else "custom-header"

    with col_icon:
        st.image(full_path, use_container_width=True) 

    with col_text:
        st.markdown(f'<p class="{text_class}">{text}</p>', unsafe_allow_html=True)

def render_sidebar_label(text, icon=""):
    st.markdown(f'<div class="sidebar-label">{icon} {text}</div>', unsafe_allow_html=True)

# ==========================================
# 🤖 Gemini API設定
# ==========================================

@st.cache_resource
def initialize_gemini():
    api_key = os.environ.get("GOOGLE_API_KEY")
    tuned_model_id = os.environ.get("TUNED_MODEL_ID")
    if not api_key: return None
    
    target_model = tuned_model_id if tuned_model_id else 'gemini-2.5-flash'
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        target_model, 
        generation_config=genai.types.GenerationConfig(temperature=0.3, max_output_tokens=4000)
    )

def call_gemini_api(model, input_text):
    prompt = f"""
    あなたは「Guardian AI」という高度な法務リスク診断システムです。
    以下の仕様の法的リスクを厳格に診断してください。
    
    【仕様】
    {input_text}
    
    【出力形式(JSON)】
    {{
        "risk_level": "High/Medium/Low",
        "summary": "履歴表示用の一言サマリー（20文字以内）",
        "laws": ["関連法1", "関連法2"],
        "reason": "詳細な理由（専門的な観点から）",
        "recommendations": ["推奨事項1", "推奨事項2", "推奨事項3"]
    }}
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "Quota exceeded" in error_msg:
            st.error("⚠️ API利用制限に達しました。")
            st.warning("Google Gemini API (無料枠) の一時的な制限です。1〜2分ほど待ってから再試行してください。")
        else:
            st.error(f"エラーが発生しました: {error_msg}")
        return None

# 結果表示
def render_result(result):
    if not result: return

    st.markdown("---")
    
    # リスクレベル
    risk = result.get('risk_level', 'Medium')
    html = f"""
    <div class="risk-container color-{risk}">
        <div class="risk-label">RISK ASSESSMENT</div>
        <div class="risk-value">{risk}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    # 関連法規
    render_icon_header("Legal Requirements", "icon_laws.png", level="subheader")
    laws_html = "".join([f'<span class="law-tag">{law}</span>' for law in result.get('laws', [])])
    st.markdown(laws_html, unsafe_allow_html=True)
    
    st.markdown("") 

    # リスク分析
    render_icon_header("Risk Analysis", "icon_analysis.png", level="subheader")
    st.write(result.get('reason'))
    
    st.markdown("") 
    
    # 推奨アクション
    st.subheader("💡 Recommendations")
    for rec in result.get('recommendations', []):
        st.info(rec)

# ==========================================
# 🖥️ メインUI構築
# ==========================================

# --- サイドバー ---
with st.sidebar:
    logo_path = get_asset_path("logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("## 🛡️ Guardian AI")

    # Quick Demo
    render_sidebar_label("Quick Demo", "⚡")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("事例: 危険"):
            st.session_state.current_input = "アプリ内でユーザーが購入したポイントを、手数料を引いて現金化し、銀行口座に振り込む機能を実装します。資金決済法の登録は行いません。"
            st.session_state.current_result = None 
            st.rerun()
    with col2:
        if st.button("事例: 安全"):
            st.session_state.current_input = "社内タスク管理ツールです。社員の氏名のみ保存し、アクセス権限を管理職に限定。退職者のデータは30日で物理削除します。"
            st.session_state.current_result = None
            st.rerun()
            
    # Legend
    render_sidebar_label("Legend", "📊")
    st.caption("🔴 High: 重大な法的リスク")
    st.caption("🟠 Medium: 注意・要確認")
    st.caption("🟢 Low: リスク低")
    
    # History
    render_sidebar_label("History", "🕒")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            risk_mark = "🔴" if item['result'].get('risk_level') == "High" else "🟠" if item['result'].get('risk_level') == "Medium" else "🟢"
            label = f"{risk_mark} {item.get('summary', '診断結果')}"
            if st.button(label, key=f"hist_{i}"):
                st.session_state.current_result = item['result']
                st.session_state.current_input = item['input']
                st.rerun()
    else:
        st.caption("履歴なし")
        
    st.markdown("---")
    if st.button("🗑️ 履歴クリア"):
        st.session_state.history = []
        st.session_state.current_result = None
        st.session_state.current_input = ""
        st.rerun()

# --- メインエリア ---

# タイトル
render_icon_header("New Assessment", "icon_new.png")

user_input = st.text_area(
    "仕様・サービス内容を入力してください", 
    value=st.session_state.current_input,
    height=150, 
    placeholder="例: ユーザーの顔写真を収集し、マーケティングに使用するアプリ..."
)

if user_input != st.session_state.current_input:
    st.session_state.current_input = user_input

# 実行ボタン
if st.button("リスク判定を実行する", type="primary"):
    if not user_input:
        st.warning("テキストを入力してください。")
    else:
        model = initialize_gemini()
        if not model:
            st.error("APIキー設定エラー: .envファイルを確認してください")
        else:
            result = None
            with st.spinner("Guardian AI が法令データベースと照合中..."):
                result = call_gemini_api(model, user_input)
            
            if result:
                summary = result.get('summary', user_input[:15]+"...")
                st.session_state.history.append({
                    "input": user_input,
                    "result": result,
                    "summary": summary,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                st.session_state.current_result = result
                st.rerun()

if st.session_state.current_result:
    render_result(st.session_state.current_result)