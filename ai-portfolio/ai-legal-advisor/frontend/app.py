"""
AI Legal Advisor - Streamlit Frontend Application
個人情報・消費者保護特化型 IT法務チェッカー
"""

import streamlit as st
from input_filter import InputFilter
import json
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="AI Legal Advisor",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# カスタムCSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-high {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        border-radius: 5px;
    }
    .risk-medium {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 1rem;
        border-radius: 5px;
    }
    .risk-low {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff9c4;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 5px solid #fbc02d;
    }
    </style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown('<div class="main-header">🏛️ AI Legal Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">個人情報・消費者保護特化型 IT法務チェッカー</div>', unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.header("📋 対応分野")
    st.markdown("""
    **✅ 対応可能な領域**
    - ✓ 個人情報保護法
    - ✓ 消費者保護（ダークパターン等）
    - ✓ アクセシビリティ
    - ✓ 金融規制
    - ✓ 契約法務
    
    **❌ 対応範囲外**
    - ✗ OSSライセンス → 弁護士に相談
    - ✗ AI倫理 → 専門家に相談
    - ✗ プログラミング技術 → 技術コミュニティへ
    """)
    
    st.divider()
    
    st.header("⚙️ 設定")
    show_debug = st.checkbox("デバッグ情報を表示", value=False)
    
    st.divider()
    
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
    <p>⚠️ 注意事項</p>
    <p>この判定結果は参考情報です。<br>
    最終的な法的判断は弁護士に<br>
    ご相談ください。</p>
    </div>
    """, unsafe_allow_html=True)

# session_stateの初期化
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''

# メインコンテンツ
st.header("📝 仕様チェック")

# サンプル入力ボタン
col1, col2, col3 = st.columns(3)

sample_texts = {
    "sample1": "ユーザーの位置情報を収集して、第三者の広告配信事業者に提供します。",
    "sample2": "解約ボタンを画面の一番下に小さく配置し、その上に『本当に解約しますか？多くの特典を失います』という警告を3回表示します。",
    "sample3": "重要な操作ボタンを画像のみで表示し、代替テキストを設定していません。"
}

with col1:
    if st.button("📍 サンプル1: 位置情報", use_container_width=True):
        st.session_state['user_input'] = sample_texts["sample1"]
        st.rerun()

with col2:
    if st.button("🚫 サンプル2: 解約UI", use_container_width=True):
        st.session_state['user_input'] = sample_texts["sample2"]
        st.rerun()

with col3:
    if st.button("♿ サンプル3: アクセシビリティ", use_container_width=True):
        st.session_state['user_input'] = sample_texts["sample3"]
        st.rerun()

# デバッグ用（動作確認後に削除）
if show_debug:
    st.write("🔍 デバッグ: session_state['user_input'] =", st.session_state['user_input'])

st.divider()

# 入力フォーム
user_input = st.text_area(
    "チェックしたい仕様を入力してください:",
    value=st.session_state['user_input'],
    height=150,
    placeholder="例: ユーザーの位置情報を収集して、第三者の広告配信事業者に提供します。",
    key="text_input"
)

# user_inputをsession_stateに同期
st.session_state['user_input'] = user_input

# クリアボタンと判定ボタン
col_clear, col_check = st.columns([1, 3])

with col_clear:
    if st.button("🗑️ クリア", use_container_width=True):
        st.session_state['user_input'] = ''
        st.rerun()

with col_check:
    check_button = st.button("🔍 リスクを判定する", type="primary", use_container_width=True)

# 判定処理
if check_button:
    if not user_input or user_input.strip() == "":
        st.warning("⚠️ 入力が空です。チェックしたい仕様を入力してください。")
    else:
        # 入力フィルタリング
        filter = InputFilter()
        is_in_scope, message, category = filter.check_scope(user_input)
        
        if not is_in_scope:
            # 対応範囲外
            st.error(f"❌ 対応範囲外: {category}")
            st.markdown(f"""
            <div class="warning-box">
            <h4>📌 メッセージ</h4>
            <p>{message}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if show_debug:
                st.divider()
                st.subheader("🐛 デバッグ情報")
                st.json({
                    "is_in_scope": is_in_scope,
                    "category": category,
                    "message": message
                })
        else:
            # 対応範囲内 - モック結果を表示
            st.success("✅ 対応範囲内の質問です")
            
            # 推測カテゴリを表示
            suggested_category = filter.suggest_category(user_input)
            if suggested_category:
                st.info(f"💡 推測カテゴリ: **{suggested_category}**")
            
            st.divider()
            
            # モックデータ（実際のモデル結果のサンプル）
            mock_result = generate_mock_result(user_input)
            
            # 結果表示
            display_result(mock_result, show_debug)

# モック結果生成関数
def generate_mock_result(input_text: str):
    """
    モックの判定結果を生成（実際のモデル出力をシミュレート）
    後でAPI呼び出しに置き換える
    """
    # キーワードベースでモックデータを選択
    if "位置情報" in input_text or "個人情報" in input_text:
        return {
            "risk_level": "中",
            "laws": ["個人情報保護法", "電気通信事業法"],
            "reason": "位置情報は個人を特定できる情報であり、収集時には目的を限定した開示が義務付けられています。また、広告配信事業者への提供は、提供先が適切な措置を講じているかの確認が必要です。",
            "recommendations": [
                "プライバシーポリシーに位置情報の収集目的を明記してください。",
                "提供先との間で個人情報の第三者提供に関する契約（NDA）を締結してください。",
                "ユーザーに対してオプトアウト（選択）機会を提供してください。"
            ],
            "inference_time": 15.2,
            "tokens_generated": 239
        }
    elif "解約" in input_text or "ダークパターン" in input_text:
        return {
            "risk_level": "高",
            "laws": ["特定商取引法", "消費者契約法"],
            "reason": "解約を不当に困難にするUI（ダークパターン）が見られ、不当な顧客囲い込みとみなされるリスクがあります。",
            "recommendations": [
                "解約ボタンは視認性の高い位置に配置してください。",
                "解約を選択したユーザーには最大限のサポートを行う設計に修正してください。",
                "警告メッセージは1回までに制限することを推奨します。"
            ],
            "inference_time": 12.8,
            "tokens_generated": 221
        }
    elif "アクセシビリティ" in input_text or "代替テキスト" in input_text or "画像" in input_text:
        return {
            "risk_level": "中",
            "laws": ["障害者差別解消法"],
            "reason": "スクリーンリーダーで画像の内容が読み上げられないことは、情報伝達における不備として認定される可能性があります。",
            "recommendations": [
                "画像ボタンにはテキストバッジを設置してください。",
                "代替テキスト（alt属性）を必ず記載してください。",
                "JIS X 8341-3に準拠した実装を行ってください。"
            ],
            "inference_time": 14.5,
            "tokens_generated": 223
        }
    else:
        # デフォルト
        return {
            "risk_level": "中",
            "laws": ["該当法を確認中"],
            "reason": "入力内容に基づいて法的リスクを分析しています。より詳細な情報があれば、精度が向上します。",
            "recommendations": [
                "具体的な仕様を追加してください。",
                "ユーザーデータの取り扱いについて明記してください。",
                "法務担当者に確認することを推奨します。"
            ],
            "inference_time": 10.0,
            "tokens_generated": 150
        }

# 結果表示関数
def display_result(result: dict, show_debug: bool = False):
    """判定結果を見やすく表示"""
    
    # リスクレベルに応じたスタイル
    risk_level = result["risk_level"]
    if "高" in risk_level:
        risk_class = "risk-high"
        risk_icon = "🔴"
    elif "中" in risk_level:
        risk_class = "risk-medium"
        risk_icon = "🟡"
    else:
        risk_class = "risk-low"
        risk_icon = "🟢"
    
    # リスクレベル表示
    st.markdown(f"""
    <div class="{risk_class}">
    <h3>{risk_icon} リスクレベル: {risk_level}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 該当法律
    st.subheader("📋 該当する可能性のある法律")
    for law in result["laws"]:
        st.markdown(f"- **{law}**")
    
    st.divider()
    
    # リスクの理由
    st.subheader("💡 リスクの理由")
    st.markdown(result["reason"])
    
    st.divider()
    
    # 推奨される対応策
    st.subheader("✅ 推奨される対応策")
    for i, rec in enumerate(result["recommendations"], 1):
        st.markdown(f"{i}. {rec}")
    
    st.divider()
    
    # コピー用のテキスト生成
    copy_text = f"""
【AI Legal Advisor 判定結果】

■ リスクレベル: {risk_level}

■ 該当する可能性のある法律:
{chr(10).join(['- ' + law for law in result["laws"]])}

■ リスクの理由:
{result["reason"]}

■ 推奨される対応策:
{chr(10).join([f'{i}. {rec}' for i, rec in enumerate(result["recommendations"], 1)])}

※ この判定結果は参考情報です。最終的な法的判断は弁護士にご相談ください。
判定日時: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}
"""
    
    # コピーボタン
    st.text_area(
        "📄 結果をコピー:",
        value=copy_text,
        height=200,
        key="copy_area"
    )
    
    # デバッグ情報
    if show_debug:
        st.divider()
        st.subheader("🐛 デバッグ情報")
        st.json({
            "risk_level": result["risk_level"],
            "laws": result["laws"],
            "inference_time": f"{result['inference_time']:.2f}秒",
            "tokens_generated": result["tokens_generated"]
        })

# フッター
st.divider()
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.9rem; padding: 2rem 0;'>
<p><strong>AI Legal Advisor Platform</strong></p>
<p>Powered by Fine-tuned Elyza-7B | Version 1.0.0 (MVP)</p>
<p>© 2026 AI Legal Advisor. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)