# 点字変換

日本語と点字を相互に変換するWebアプリケーションです。

日本語から点字への変換には、外部ライブラリの [libkuraji](https://github.com/nishimotz/libkuraji) を使用しています。

## 機能

### 日本語 → 点字

* 漢字を含む日本語文章を入力できます。
* 入力した日本語文章から、かなと点字を自動生成します。
* 生成されたかなをユーザーが編集できます。
* 編集したかなをもとに点字を修正できます。

### 点字 → 日本語

* 点字を入力し、日本語へ変換できます。
* 点字の変換処理は本プロジェクトで実装しています。
* 数符・外字符・大文字符などの識別符号を考慮して変換します。

## 使用技術

* Python
* Django
* [libkuraji](https://github.com/nishimotz/libkuraji)

## セットアップ

### 1. 仮想環境の作成

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

`requirements.txt`には、`libkuraji`のintegration機能を含めて以下のように記載します。

```text
libkuraji[integration]
```

### 3. 環境変数の設定

漢字を含む日本語の点訳に必要なJTalk拡張辞書連携を有効にするため、以下の環境変数を設定します。

```text
LIBKURAJI_INTEGRATION=1
```

開発環境では`.env`などを利用できます。

`.env.example`には必要な環境変数の例を記載し、`.env`自体はGitで管理しないようにしてください。

### 4. アプリケーションの起動

```bash
python manage.py runserver
```

## 外部ライブラリ

### libkuraji

本プロジェクトでは、日本語から点字への変換に [libkuraji](https://github.com/nishimotz/libkuraji) を使用しています。

`libkuraji`は、漢字・かなが混在した日本語文章を日本語6点式点字へ変換するPythonライブラリです。

* リポジトリ: https://github.com/nishimotz/libkuraji
* 作者: Takuya Nishimoto
* ライセンス: BSD 3-Clause License

本プロジェクトでは、`libkuraji`を外部依存パッケージとして`pip`からインストールして利用しています。

`libkuraji`のJTalk拡張辞書連携については、[libkuraji-jtalk-dic](https://github.com/nishimotz/libkuraji-jtalk-dic) が使用されます。

## ライセンス

本プロジェクトのライセンスは現在未定です。

本プロジェクトで利用している第三者ソフトウェアについては、それぞれのライセンス条件が適用されます。
