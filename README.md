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

* Python 3.13
* Django
* uv（Python パッケージ・仮想環境管理）
* [libkuraji](https://github.com/nishimotz/libkuraji)

## セットアップ

### 事前準備

以下をインストールしてください。

- Git
- Python 3.13
- [uv](https://docs.astral.sh/uv/)

### 1. リポジトリの取得

`libkuraji` は Git サブモジュールとして管理しているため、`--recurse-submodules` を付けて取得してください。

```bash
git clone --recurse-submodules https://github.com/gdsc-osaka/Braille-Translation.git
cd Braille-Translation
```

すでにリポジトリを取得していて、サブモジュールが取得されていない場合は、次のコマンドを実行してください。

```bash
git submodule update --init --recursive
```

### 2. 仮想環境の作成と依存パッケージのインストール

リポジトリのルートディレクトリで、次のコマンドを実行してください。

```bash
uv sync --frozen
```

これにより、`.venv` が作成され、`uv.lock` に記録された依存関係に従ってパッケージがインストールされます。

`uv.lock` を使って依存関係を固定することで、開発メンバー間で環境をそろえやすくなります。

### 3. 環境変数の設定

リポジトリのルートディレクトリにある `.env.example` を参考に、`.env` ファイルを作成してください。

`.env` には、次の環境変数を設定します。

```dotenv
DJANGO_SECRET_KEY=replace-with-a-random-secret-key
LIBKURAJI_INTEGRATION=1
DJANGO_DEBUG=True
```

- `DJANGO_SECRET_KEY`：Django が使用する秘密鍵です。実際の値を設定してください。
- `LIBKURAJI_INTEGRATION=1`：libkuraji の integration 機能を有効にします。
- `DJANGO_DEBUG=True`：ローカル開発用にデバッグモードを有効にします。本番環境では `False` にしてください。

### 4. Django の設定確認

次のコマンドを実行してください。

```bash
uv run python manage.py check
```

エラーが表示されなければ、Django の基本的な設定確認は完了です。

### 5. アプリケーションの起動

```bash
uv run python manage.py runserver
```

ブラウザで [http://127.0.0.1:8000/](http://127.0.0.1:8000/) にアクセスしてください。

## 依存関係の管理

本プロジェクトでは、依存関係の管理に uv を使用します。

### パッケージの追加

```bash
uv add パッケージ名
```

開発時のみ必要なパッケージを追加する場合は、次のようにします。

```bash
uv add --dev パッケージ名
```

### パッケージの削除

```bash
uv remove パッケージ名
```

### 依存関係の同期

`pyproject.toml` や `uv.lock` が更新された場合は、次のコマンドで環境を同期できます。

```bash
uv sync --frozen
```

`pyproject.toml` の依存関係を変更した場合は、変更に応じて `uv.lock` も更新し、両方のファイルを Git にコミットしてください。

通常の環境構築では、ロックファイルに記録された依存関係を使うため、`uv sync --frozen` を使用してください。

## 外部ライブラリ

### libkuraji

本プロジェクトでは、日本語から点字への変換に [libkuraji](https://github.com/nishimotz/libkuraji) を使用しています。

`libkuraji`は、漢字・かなが混在した日本語文章を日本語6点式点字へ変換するPythonライブラリです。

* リポジトリ: [https://github.com/nishimotz/libkuraji](https://github.com/nishimotz/libkuraji)
* 作者: Takuya Nishimoto
* ライセンス: BSD 3-Clause License

本プロジェクトでは、`libkuraji` を Git サブモジュールとして取得し、uv からローカルのライブラリとしてインストールして利用します。

`libkuraji`のJTalk拡張辞書連携については、[libkuraji-jtalk-dic](https://github.com/nishimotz/libkuraji-jtalk-dic) が使用されます。

## ライセンス

本プロジェクトのライセンスは現在未定です。

本プロジェクトで利用している第三者ソフトウェアについては、それぞれのライセンス条件が適用されます。
