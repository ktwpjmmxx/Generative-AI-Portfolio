"""
利用可能なGemini APIモデルを確認するスクリプト
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("❌ エラー: GOOGLE_API_KEY が設定されていません")
    print("\n.env ファイルに以下の形式で設定してください:")
    print("GOOGLE_API_KEY=your_actual_api_key_here")
    exit(1)

print(f"✅ APIキー確認: {api_key[:4]}...{api_key[-4:]}")
print("\n" + "="*60)
print("利用可能なGemini モデル一覧")
print("="*60 + "\n")

try:
    genai.configure(api_key=api_key)
    
    # 利用可能なモデルをリスト
    models = genai.list_models()
    
    gemini_models = []
    for model in models:
        # generateContent をサポートしているモデルのみ表示
        if 'generateContent' in model.supported_generation_methods:
            gemini_models.append(model)
            print(f"📝 モデル名: {model.name}")
            print(f"   表示名: {model.display_name}")
            print(f"   説明: {model.description}")
            print(f"   サポートメソッド: {', '.join(model.supported_generation_methods)}")
            print()
    
    if not gemini_models:
        print("⚠️ generateContent をサポートするモデルが見つかりませんでした")
    else:
        print("="*60)
        print(f"\n✅ 合計 {len(gemini_models)} 個のモデルが利用可能です\n")
        print("【推奨モデル名（app_gemini.py で使用）】")
        for model in gemini_models[:3]:  # 最初の3つを表示
            # "models/" プレフィックスを除去
            model_name = model.name.replace("models/", "")
            print(f"  • {model_name}")

except Exception as e:
    print(f"❌ エラーが発生しました: {e}")
    print("\n【考えられる原因】")
    print("1. APIキーが無効または期限切れ")
    print("2. インターネット接続の問題")
    print("3. Google AI Studio でAPIが有効化されていない")
