# AI Legal Advisor Platform

**個人情報・消費者保護特化型 IT法務チェッカー**

Google Gemini API (2.5 Flash) およびファインチューニング済みLLMを活用した、IT法務リスク判定システム。開発仕様書やサービス設計案を入力することで、法的リスク、関連法規、推奨アクションを即座に提示します。

---

## プロジェクト概要

このプロジェクトは、AIを活用して開発段階における法的リスクを早期発見（シフトレフト）することを目的としたWebアプリケーションです。

現在はプロトタイプフェーズとして、推論エンジンに「Gemini 2.5 Flash」を採用し、高速かつ高精度な診断を実現しています。将来的には、特定の法務ドメインでファインチューニングを行った独自のローカルLLM（Elyza-7Bベース）への切り替えも可能なアーキテクチャを採用しています。

### 主な特徴

* **即時リスク診断**: 仕様テキストを入力するだけで、数秒以内に「High/Medium/Low」のリスク判定を行います。
* **具体的根拠の提示**: 判定理由とともに、日本の法律（個人情報保護法、資金決済法など）に基づいた法的根拠を提示します。
* **フィルタリング機能**: AI倫理や技術的な実装詳細など、対応範囲外の入力を事前に検知・除外します。
* **ミニマルなUI**: チャット形式のシンプルなインターフェースで、法務担当者以外の開発者でも直感的に利用可能です。

---

## 対応範囲

本システムは以下の領域における診断に特化しています。

### 対応可能な領域
1.  **個人情報保護** (データの収集・利用・第三者提供、同意取得)
2.  **消費者保護** (ダークパターン、不当な解約フロー、有利誤認表示)
3.  **アクセシビリティ** (ウェブアクセシビリティ、障害者差別解消法)
4.  **金融規制** (資金決済法、ポイント・コイン発行、暗号資産)
5.  **契約法務** (利用規約の不当条項、信義則違反)

### 対応範囲外
* OSSライセンスの互換性判定
* 高度なAI倫理・バイアス判定
* プログラミングコードのセキュリティ診断

---

## システム構成

### アーキテクチャ (Prototype)

現在はStreamlitとGemini APIを直接接続する構成で稼働しています。

```
[User] -> [Streamlit Client (Frontend)] -> [Input Filter] -> [Gemini API (2.5 Flash)]
```

※ **Local LLM Mode**: 構成を変更することで、ローカル環境（GPUマシン）またはGoogle Colab上で稼働する自作FTモデル（Transformers/Elyza-7B）での推論も可能です。

### ディレクトリ構成

```
ai-legal-advisor/
├── app_gemini.py        # メインアプリケーション (Gemini API版)
├── app_local_llm.py     # メインアプリケーション (ローカルLLM版)
├── input_filter.py      # 入力フィルタリングモジュール
├── check_models.py      # 利用可能モデル確認用スクリプト
├── .env                 # 環境変数設定 (API Key等)
└── requirements.txt     # 依存パッケージ
```

---

## セットアップと実行

### 前提条件
* Python 3.10以上
* Google API Key (Gemini)

### インストール手順

1.  **リポジトリのクローン**
    ```bash
    git clone [repository_url]
    cd ai-legal-advisor
    ```

2.  **依存パッケージのインストール**
    ```bash
    pip install -r requirements.txt
    ```

3.  **環境変数の設定**
    `.env` ファイルを作成し、APIキーを設定します。
    ```env
    GOOGLE_API_KEY=your_api_key_here
    # TUNED_MODEL_ID=tunedModels/your-model-id (FTモデル使用時のみ)
    ```

4.  **アプリケーションの起動**
    ```bash
    streamlit run app_gemini.py
    ```

---

## 開発ステータス

### 実装済み
- [x] Streamlitによるチャット形式UIの実装
- [x] Gemini 2.5 Flash APIとの連携
- [x] InputFilterによるスコープ外検知ロジック
- [x] 長文回答に対応したトークン数調整
- [x] JSON形式での構造化データ出力

### 今後のロードマップ
- [ ] ファインチューニング済みモデル(Elyza-7B)のAPI化・統合
- [ ] 診断履歴のログ保存機能
- [ ] レポートのPDF出力機能

---

## 使用技術

* **Frontend**: Streamlit
* **LLM API**: Google Gemini API (gemini-2.5-flash)
* **Local LLM (Option)**: Hugging Face Transformers, PyTorch, BitsAndBytes
* **Language**: Python 3.10+

---

## ライセンス

MIT License

*最終更新: 2026年1月21日*