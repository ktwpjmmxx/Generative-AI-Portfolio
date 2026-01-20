"""
入力フィルタリングモジュール
対応範囲外のキーワードを検出し、適切なメッセージを返す
"""

from typing import Tuple, Optional
import re


class InputFilter:
    """
    ユーザー入力が対応範囲内かどうかを判定するクラス
    
    対応範囲:
    - 個人情報保護法
    - 消費者保護（ダークパターン等）
    - アクセシビリティ
    - 金融規制
    - 契約法務
    """
    
    def __init__(self):
        """対応範囲外のキーワードと対応するメッセージを定義"""
        self.out_of_scope_keywords = {
            # OSSライセンス関連
            "ライセンス": {
                "message": "OSSライセンスに関するご質問は、専門の知的財産弁護士にご相談ください。",
                "category": "OSS License"
            },
            "GPL": {
                "message": "OSSライセンスに関するご質問は、専門の知的財産弁護士にご相談ください。",
                "category": "OSS License"
            },
            "MIT": {
                "message": "OSSライセンスに関するご質問は、専門の知的財産弁護士にご相談ください。",
                "category": "OSS License"
            },
            "Apache": {
                "message": "OSSライセンスに関するご質問は、専門の知的財産弁護士にご相談ください。",
                "category": "OSS License"
            },
            "BSD": {
                "message": "OSSライセンスに関するご質問は、専門の知的財産弁護士にご相談ください。",
                "category": "OSS License"
            },
            
            # プログラミング技術関連
            "React": {
                "message": "プログラミング技術に関するご質問は、技術コミュニティやドキュメントをご参照ください。",
                "category": "Programming"
            },
            "Docker": {
                "message": "プログラミング技術に関するご質問は、技術コミュニティやドキュメントをご参照ください。",
                "category": "Programming"
            },
            "Kubernetes": {
                "message": "プログラミング技術に関するご質問は、技術コミュニティやドキュメントをご参照ください。",
                "category": "Programming"
            },
            "Python": {
                "message": "プログラミング技術に関するご質問は、技術コミュニティやドキュメントをご参照ください。",
                "category": "Programming"
            },
            "JavaScript": {
                "message": "プログラミング技術に関するご質問は、技術コミュニティやドキュメントをご参照ください。",
                "category": "Programming"
            },
            
            # AI倫理関連
            "AI判定": {
                "message": "AIによる自動判定の倫理的側面については、AI倫理専門家にご相談ください。",
                "category": "AI Ethics"
            },
            "顔認証": {
                "message": "生体認証の倫理的側面については、AI倫理専門家にご相談ください。",
                "category": "AI Ethics"
            },
            "アルゴリズム差別": {
                "message": "アルゴリズムの倫理的側面については、AI倫理専門家にご相談ください。",
                "category": "AI Ethics"
            },
            "バイアス": {
                "message": "AIバイアスの倫理的側面については、AI倫理専門家にご相談ください。",
                "category": "AI Ethics"
            },
        }
        
        # 対応範囲内のキーワード（参考情報）
        self.in_scope_keywords = {
            "個人情報": ["個人情報保護法", "プライバシーポリシー", "同意取得"],
            "消費者保護": ["ダークパターン", "解約", "利用規約", "不当条項"],
            "アクセシビリティ": ["WCAG", "障害者差別解消法", "音声読み上げ"],
            "金融規制": ["電子決済", "暗号資産", "資金決済法"],
            "契約": ["SaaS", "利用規約", "信義則"],
        }
    
    def check_scope(self, input_text: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        入力テキストが対応範囲内かチェック
        
        Args:
            input_text: ユーザーの入力テキスト
            
        Returns:
            Tuple[bool, Optional[str], Optional[str]]: 
                - is_in_scope: 対応範囲内ならTrue
                - message: 対応範囲外の場合のメッセージ
                - category: 対応範囲外のカテゴリ
        """
        # 空文字チェック
        if not input_text or input_text.strip() == "":
            return False, "入力が空です。チェックしたい仕様を入力してください。", None
        
        # 対応範囲外のキーワードをチェック
        for keyword, info in self.out_of_scope_keywords.items():
            # 大文字小文字を区別せずに検索
            if re.search(keyword, input_text, re.IGNORECASE):
                return False, info["message"], info["category"]
        
        # 対応範囲内と判定
        return True, None, None
    
    def get_in_scope_categories(self) -> dict:
        """対応可能なカテゴリ一覧を取得"""
        return self.in_scope_keywords
    
    def suggest_category(self, input_text: str) -> Optional[str]:
        """
        入力テキストから最も関連性の高いカテゴリを推測
        
        Args:
            input_text: ユーザーの入力テキスト
            
        Returns:
            Optional[str]: 推測されたカテゴリ名（該当なしの場合None）
        """
        max_matches = 0
        suggested_category = None
        
        for category, keywords in self.in_scope_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in input_text)
            if matches > max_matches:
                max_matches = matches
                suggested_category = category
        
        return suggested_category if max_matches > 0 else None


# テスト用のメイン関数
if __name__ == "__main__":
    # フィルターのインスタンス作成
    filter = InputFilter()
    
    # テストケース
    test_cases = [
        "ユーザーの位置情報を収集して広告配信に利用します",  # 対応範囲内
        "GPLライセンスのコードを利用しても大丈夫ですか？",  # 対応範囲外（OSS）
        "Reactコンポーネントの実装方法を教えてください",     # 対応範囲外（技術）
        "顔認証システムを導入したいのですが",              # 対応範囲外（AI倫理）
        "解約ボタンが見つけにくい位置にあります",          # 対応範囲内
        "",                                               # 空文字
    ]
    
    print("=" * 60)
    print("入力フィルタリングテスト")
    print("=" * 60)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n【テスト {i}】")
        print(f"入力: {test_input if test_input else '(空文字)'}")
        
        is_in_scope, message, category = filter.check_scope(test_input)
        
        if is_in_scope:
            print("✅ 対応範囲内")
            suggested = filter.suggest_category(test_input)
            if suggested:
                print(f"   推測カテゴリ: {suggested}")
        else:
            print(f"❌ 対応範囲外")
            if category:
                print(f"   カテゴリ: {category}")
            print(f"   メッセージ: {message}")
    
    print("\n" + "=" * 60)
    print("対応可能なカテゴリ:")
    print("=" * 60)
    for category, keywords in filter.get_in_scope_categories().items():
        print(f"✓ {category}: {', '.join(keywords)}")